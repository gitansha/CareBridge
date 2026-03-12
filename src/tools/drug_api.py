"""
Drug & Medication API tool — wraps RxNorm (NIH) and OpenFDA APIs.

- RxNorm: drug name ↔ RxCUI mapping, drug-drug interaction checks
- OpenFDA: drug label information (warnings, contraindications, interactions)
"""

import requests
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

RXNORM_BASE = "https://rxnav.nlm.nih.gov/REST"
OPENFDA_BASE = "https://api.fda.gov/drug"

SCHEMA_DRUG_INTERACTION = {
    "type": "function",
    "function": {
        "name": "check_drug_interactions",
        "description": (
            "Check for known drug-drug interactions between a list of medications. "
            "Provide drug names or RxCUI codes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "drug_list": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of drug names (e.g. ['Warfarin', 'Aspirin'])",
                },
            },
            "required": ["drug_list"],
        },
    },
}

SCHEMA_DRUG_INFO = {
    "type": "function",
    "function": {
        "name": "get_drug_info",
        "description": "Get detailed drug label information from OpenFDA (warnings, contraindications, interactions).",
        "parameters": {
            "type": "object",
            "properties": {
                "drug_name": {"type": "string", "description": "Generic drug name (e.g. 'warfarin')"},
            },
            "required": ["drug_name"],
        },
    },
}

SCHEMA_DRUG_LOOKUP = {
    "type": "function",
    "function": {
        "name": "lookup_drug_rxcui",
        "description": "Look up the RxCUI identifier for a drug by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "drug_name": {"type": "string", "description": "Drug name to look up"},
            },
            "required": ["drug_name"],
        },
    },
}


def _get_rxcui(drug_name):
    """Resolve a drug name to an RxCUI via RxNorm."""
    try:
        r = requests.get(
            f"{RXNORM_BASE}/rxcui.json",
            params={"name": drug_name},
            timeout=10,
            verify=False,
        )
        r.raise_for_status()
        ids = r.json().get("idGroup", {}).get("rxnormId", [])
        return ids[0] if ids else None
    except Exception as e:
        logger.warning(f"RxCUI lookup failed for {drug_name}: {e}")
        return None


def lookup_drug_rxcui(drug_name):
    rxcui = _get_rxcui(drug_name)
    if rxcui:
        return {"drug_name": drug_name, "rxcui": rxcui}
    return {"drug_name": drug_name, "rxcui": None, "message": "Could not resolve RxCUI. Try the generic drug name."}


def check_drug_interactions(drug_list):
    """Check interactions between multiple drugs using RxNorm interaction API."""
    # Resolve all drug names to RxCUIs
    rxcuis = {}
    for drug in drug_list:
        rxcui = _get_rxcui(drug)
        if rxcui:
            rxcuis[drug] = rxcui

    if len(rxcuis) < 2:
        return {
            "checked": False,
            "message": f"Need at least 2 resolved drugs for interaction check. Resolved: {list(rxcuis.keys())}",
        }

    # Use the RxNorm interaction list endpoint
    rxcui_str = "+".join(rxcuis.values())
    try:
        r = requests.get(
            f"{RXNORM_BASE}/interaction/list.json",
            params={"rxcuis": rxcui_str},
            timeout=15,
            verify=False,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"checked": False, "message": f"RxNorm API error: {e}"}

    interactions = []
    for group in data.get("fullInteractionTypeGroup", []):
        for itype in group.get("fullInteractionType", []):
            for pair in itype.get("interactionPair", []):
                drugs = [c.get("minConcept", {}).get("name", "?")
                         if isinstance(c, dict) else "?"
                         for c in pair.get("interactionConcept", [])]
                # Extract drug names from interactionConcept properly
                drug_names = []
                for ic in pair.get("interactionConcept", []):
                    mc = ic.get("minConceptItem", {})
                    drug_names.append(mc.get("name", "Unknown"))

                interactions.append({
                    "drugs": drug_names,
                    "severity": pair.get("severity", "N/A"),
                    "description": pair.get("description", "No description available."),
                })

    return {
        "checked": True,
        "drug_list": drug_list,
        "resolved_rxcuis": rxcuis,
        "interaction_count": len(interactions),
        "interactions": interactions[:10],  # cap at 10
    }


def get_drug_info(drug_name):
    """Get drug label information from OpenFDA."""
    try:
        r = requests.get(
            f"{OPENFDA_BASE}/label.json",
            params={"search": f"openfda.generic_name:{drug_name}", "limit": 1},
            timeout=10,
            verify=False,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"found": False, "message": f"OpenFDA API error: {e}"}

    results = data.get("results", [])
    if not results:
        return {"found": False, "message": f"No label found for '{drug_name}'."}

    result = results[0]
    openfda = result.get("openfda", {})

    return {
        "found": True,
        "drug_name": drug_name,
        "brand_names": openfda.get("brand_name", []),
        "generic_names": openfda.get("generic_name", []),
        "drug_class": openfda.get("pharm_class_epc", []),
        "warnings": (result.get("warnings", ["N/A"])[0])[:500],
        "contraindications": (result.get("contraindications", ["N/A"])[0])[:500],
        "drug_interactions": (result.get("drug_interactions", ["N/A"])[0])[:500],
        "adverse_reactions": (result.get("adverse_reactions", ["N/A"])[0])[:300],
    }
