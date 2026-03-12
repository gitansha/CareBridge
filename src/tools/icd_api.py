"""
ICD-10/11 classification tool — wraps the WHO ICD API.

Requires OAuth2 credentials from https://icd.who.int/icdapi
Falls back to a built-in common-codes lookup when credentials are unavailable.
"""

import requests
import logging
from config.settings import ICD_CLIENT_ID, ICD_CLIENT_SECRET

logger = logging.getLogger(__name__)

TOKEN_URL = "https://icdaccessmanagement.who.int/connect/token"
ICD_API_BASE = "https://id.who.int/icd"

SCHEMA_SEARCH_ICD = {
    "type": "function",
    "function": {
        "name": "search_icd_code",
        "description": (
            "Search for an ICD-10/ICD-11 code given a diagnosis description. "
            "Returns matching codes with descriptions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Diagnosis or condition description (e.g. 'type 2 diabetes')",
                },
                "version": {
                    "type": "string",
                    "enum": ["icd10", "icd11"],
                    "description": "ICD version to search (default: icd10)",
                },
            },
            "required": ["query"],
        },
    },
}

SCHEMA_GET_ICD = {
    "type": "function",
    "function": {
        "name": "get_icd_details",
        "description": "Get details for a specific ICD code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "ICD code (e.g. 'E11.9')"},
            },
            "required": ["code"],
        },
    },
}

# ── Common ICD-10 codes fallback ────────────────────────────────────────────

COMMON_ICD10 = {
    "I10": "Essential (primary) hypertension",
    "I20.0": "Unstable angina",
    "I20.8": "Other forms of angina pectoris",
    "I21.09": "ST elevation myocardial infarction involving other coronary artery of anterior wall",
    "I25.2": "Old myocardial infarction",
    "I25.9": "Chronic ischemic heart disease, unspecified",
    "I42.7": "Cardiomyopathy due to drug and external agent",
    "I48.91": "Unspecified atrial fibrillation",
    "E11.9": "Type 2 diabetes mellitus without complications",
    "E11.40": "Type 2 diabetes mellitus with diabetic neuropathy, unspecified",
    "E11.65": "Type 2 diabetes mellitus with hyperglycemia",
    "E78.5": "Hyperlipidemia, unspecified",
    "G20": "Parkinson's disease",
    "G40.109": "Localization-related (focal) (partial) idiopathic epilepsy",
    "G41.0": "Grand mal status epilepticus",
    "G43.709": "Chronic migraine without aura, not intractable",
    "G63": "Polyneuropathy in diseases classified elsewhere",
    "J45.41": "Moderate persistent asthma with acute exacerbation",
    "J46": "Status asthmaticus",
    "M16.11": "Primary osteoarthritis, right hip",
    "M17.11": "Primary osteoarthritis, right knee",
    "M51.16": "Intervertebral disc disorders with radiculopathy, lumbar region",
    "S82.101A": "Unspecified fracture of upper end of right tibia, initial encounter",
    "S83.209A": "Unspecified tear of unspecified meniscus, initial encounter",
    "S93.401A": "Unspecified sprain of right ankle, initial encounter",
    "C34.90": "Malignant neoplasm of unspecified part of unspecified bronchus or lung",
    "C50.919": "Malignant neoplasm of unspecified site of unspecified female breast",
    "C61": "Malignant neoplasm of prostate",
    "R63.4": "Abnormal weight loss",
    "T78.01": "Anaphylactic reaction due to peanuts",
    "T78.2": "Anaphylactic shock, unspecified",
    "Z09": "Encounter for follow-up examination after completed treatment for conditions other than malignant neoplasm",
    "Z34.01": "Encounter for supervision of normal first pregnancy, first trimester",
}


def _get_who_token():
    """Get OAuth2 token from WHO ICD API."""
    if not ICD_CLIENT_ID or not ICD_CLIENT_SECRET:
        return None
    try:
        r = requests.post(TOKEN_URL, data={
            "client_id": ICD_CLIENT_ID,
            "client_secret": ICD_CLIENT_SECRET,
            "scope": "icdapi_access",
            "grant_type": "client_credentials",
        }, timeout=10)
        r.raise_for_status()
        return r.json().get("access_token")
    except Exception as e:
        logger.warning(f"WHO ICD token error: {e}")
        return None


def search_icd_code(query, version="icd10"):
    """Search for ICD codes matching a description."""
    # Try WHO API first
    token = _get_who_token()
    if token:
        try:
            release = "2019-covid-expanded" if version == "icd10" else "2024-01"
            url = f"{ICD_API_BASE}/release/{version}/{release}/search"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Accept-Language": "en",
                "API-Version": "v2",
            }
            r = requests.get(url, headers=headers, params={
                "q": query,
                "subtreeFilterUsesFoundationDescendants": "false",
                "includeKeywordResult": "false",
                "flatResults": "true",
                "highlightingEnabled": "false",
            }, timeout=10)
            r.raise_for_status()
            data = r.json()

            results = []
            for item in data.get("destinationEntities", [])[:10]:
                results.append({
                    "code": item.get("theCode", ""),
                    "title": item.get("title", ""),
                    "score": item.get("score", 0),
                })
            return {"source": "WHO API", "version": version, "query": query, "results": results}
        except Exception as e:
            logger.warning(f"WHO API search failed: {e}")

    # Fallback to local lookup
    query_lower = query.lower()
    matches = []
    for code, desc in COMMON_ICD10.items():
        if query_lower in desc.lower() or query_lower in code.lower():
            matches.append({"code": code, "title": desc, "score": 1.0})

    return {
        "source": "local_fallback",
        "version": "icd10",
        "query": query,
        "results": matches,
        "note": "WHO API credentials not configured. Using local common-codes fallback." if not token else None,
    }


def get_icd_details(code):
    """Get details for a specific ICD code."""
    # Local first
    if code in COMMON_ICD10:
        return {"code": code, "title": COMMON_ICD10[code], "source": "local"}

    # Try WHO API
    token = _get_who_token()
    if token:
        try:
            url = f"{ICD_API_BASE}/release/10/2019-covid-expanded/{code}"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Accept-Language": "en",
                "API-Version": "v2",
            }
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            return {
                "code": code,
                "title": data.get("title", {}).get("@value", ""),
                "definition": data.get("definition", {}).get("@value", ""),
                "source": "WHO API",
            }
        except Exception:
            pass

    return {"code": code, "title": "Unknown", "source": "not_found"}
