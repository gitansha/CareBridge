import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os

es = Elasticsearch(
    "",
    api_key="",
)

DATA_DIR = "C:\\Gitansha\\Gitansha\\NTU\\projects\\Hackathon\\Elastic\\synthea_dataset\\output\\csv"  # folder where your CSVs live

# ── Index mappings ────────────────────────────────────────────────────────────

MAPPINGS = {
    "patients": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "first": {"type": "text"},
                "last": {"type": "text"},
                "full_name": {"type": "text"},
                "birthdate": {"type": "date", "format": "yyyy-MM-dd"},
                "gender": {"type": "keyword"},
                "race": {"type": "keyword"},
                "city": {"type": "keyword"},
                "country": {"type": "keyword"},
                "clinical_summary": {"type": "text"},  # LLM-ready summary
                "ssn": {"type": "keyword", "index": False},  # stored, not searchable
            }
        }
    },
    "allergies": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "start": {
                    "type": "date",
                    "format": "yyyy-MM-dd||strict_date_optional_time",
                },
                "code": {"type": "keyword"},
                "description": {"type": "text"},
                "type": {"type": "keyword"},
                "category": {"type": "keyword"},
                "severity1": {"type": "keyword"},
                "reaction_desc": {"type": "text"},
            }
        }
    },
    "conditions": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "start": {"type": "date", "format": "yyyy-MM-dd"},
                "stop": {"type": "date", "format": "yyyy-MM-dd", "null_value": None},
                "code": {"type": "keyword"},
                "description": {"type": "text"},
                "system": {"type": "keyword"},
                "active": {"type": "boolean"},
            }
        }
    },
    "medications": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "start": {"type": "date", "format": "strict_date_optional_time"},
                "stop": {"type": "date", "format": "strict_date_optional_time"},
                "code": {"type": "keyword"},
                "description": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "base_cost": {"type": "float"},
                "reason_description": {"type": "text"},
                "active": {"type": "boolean"},
            }
        }
    },
    "encounters": {
        "mappings": {
            "properties": {
                "encounter_id": {"type": "keyword"},
                "patient_id": {"type": "keyword"},
                "start": {"type": "date", "format": "strict_date_optional_time"},
                "stop": {"type": "date", "format": "strict_date_optional_time"},
                "provider_id": {"type": "keyword"},
                "encounter_class": {"type": "keyword"},
                "description": {"type": "text"},
                "reason_description": {"type": "text"},
                "total_claim_cost": {"type": "float"},
            }
        }
    },
    "observations": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "date": {"type": "date", "format": "strict_date_optional_time"},
                "category": {"type": "keyword"},
                "code": {"type": "keyword"},
                "description": {"type": "text"},
                "value": {"type": "text"},  # mixed numeric/text in Synthea
                "units": {"type": "keyword"},
                "type": {"type": "keyword"},
            }
        }
    },
    "procedures": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "start": {"type": "date", "format": "strict_date_optional_time"},
                "code": {"type": "keyword"},
                "description": {"type": "text"},
                "base_cost": {"type": "float"},
                "reason_description": {"type": "text"},
            }
        }
    },
    "providers": {
        "mappings": {
            "properties": {
                "provider_id": {"type": "keyword"},
                "name": {"type": "text"},
                "gender": {"type": "keyword"},
                "speciality": {"type": "keyword"},
                "city": {"type": "keyword"},
                "organization": {"type": "keyword"},
                "encounters": {"type": "integer"},
            }
        }
    },
    "immunizations": {
        "mappings": {
            "properties": {
                "patient_id": {"type": "keyword"},
                "encounter_id": {"type": "keyword"},
                "date": {"type": "date", "format": "strict_date_optional_time"},
                "code": {"type": "keyword"},
                "description": {"type": "text"},
                "base_cost": {"type": "float"},
            }
        }
    },
}

# ── Transform functions (one per CSV) ─────────────────────────────────────────


def load_patients(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["Id"],
                "first": r.get("FIRST", ""),
                "last": r.get("LAST", ""),
                "full_name": f"{r.get('FIRST','')} {r.get('LAST','')}".strip(),
                "birthdate": r.get("BIRTHDATE"),
                "gender": r.get("GENDER"),
                "race": r.get("RACE"),
                "city": r.get("city", r.get("CITY", "")),
                "country": r.get("country", "Singapore"),
                "clinical_summary": r.get("clinical_summary", ""),
                "ssn": r.get("SSN", ""),
            }
        )
    return docs


def load_allergies(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "start": r.get("START"),
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "type": r.get("TYPE", ""),
                "category": r.get("CATEGORY", ""),
                "severity1": r.get("SEVERITY1", ""),
                "reaction_desc": r.get("DESCRIPTION1", ""),
            }
        )
    return docs


def load_conditions(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "start": r.get("START"),
                "stop": r.get("STOP") if pd.notna(r.get("STOP")) else None,
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "system": r.get("SYSTEM", ""),
                "active": pd.isna(r.get("STOP")),  # active if no stop date
            }
        )
    return docs


def load_medications(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "start": r.get("START"),
                "stop": r.get("STOP") if pd.notna(r.get("STOP")) else None,
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "base_cost": r.get("BASE_COST"),
                "reason_description": r.get("REASONDESCRIPTION", ""),
                "active": pd.isna(r.get("STOP")),
            }
        )
    return docs


def load_encounters(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "encounter_id": r["Id"],
                "patient_id": r["PATIENT"],
                "start": r.get("START"),
                "stop": r.get("STOP"),
                "provider_id": r.get("PROVIDER"),
                "encounter_class": r.get("ENCOUNTERCLASS"),
                "description": r.get("DESCRIPTION", ""),
                "reason_description": r.get("REASONDESCRIPTION", ""),
                "total_claim_cost": r.get("TOTAL_CLAIM_COST"),
            }
        )
    return docs


def load_observations(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "date": r.get("DATE"),
                "category": r.get("CATEGORY", ""),
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "value": str(r.get("VALUE", "")),
                "units": r.get("UNITS", ""),
                "type": r.get("TYPE", ""),
            }
        )
    return docs


def load_procedures(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "start": r.get("START"),
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "base_cost": r.get("BASE_COST"),
                "reason_description": r.get("REASONDESCRIPTION", ""),
            }
        )
    return docs


def load_providers(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "provider_id": r["Id"],
                "name": r.get("NAME", ""),
                "gender": r.get("GENDER", ""),
                "speciality": r.get("SPECIALITY", ""),
                "city": r.get("CITY", ""),
                "organization": r.get("ORGANIZATION", ""),
                "encounters": r.get("ENCOUNTERS", 0),
            }
        )
    return docs


def load_immunizations(path):
    df = pd.read_csv(path)
    docs = []
    for _, r in df.iterrows():
        docs.append(
            {
                "patient_id": r["PATIENT"],
                "encounter_id": r["ENCOUNTER"],
                "date": r.get("DATE"),
                "code": str(r.get("CODE", "")),
                "description": r.get("DESCRIPTION", ""),
                "base_cost": r.get("BASE_COST"),
            }
        )
    return docs


# ── Bulk ingest ───────────────────────────────────────────────────────────────

LOADERS = {
    "patients": ("patients_sg_ai_ready.csv", load_patients),
    "allergies": ("allergies.csv", load_allergies),
    "conditions": ("conditions.csv", load_conditions),
    "medications": ("medications.csv", load_medications),
    "encounters": ("encounters.csv", load_encounters),
    "observations": ("observations.csv", load_observations),
    "procedures": ("procedures.csv", load_procedures),
    "providers": ("providers.csv", load_providers),
    "immunizations": ("immunizations.csv", load_immunizations),
}


def ingest_all():
    for index_name, (filename, loader_fn) in LOADERS.items():
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            print(f"SKIP {index_name} — file not found: {filepath}")
            continue

        # Create index with mapping
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(f"Dropped existing index: {index_name}")

        es.indices.create(index=index_name, body=MAPPINGS[index_name])
        print(f"Created index: {index_name}")

        # Load and bulk index
        docs = loader_fn(filepath)
        actions = [
            {"_index": index_name, "_source": doc} for doc in docs if doc  # skip empty
        ]

        success, errors = helpers.bulk(es, actions, raise_on_error=False)
        print(f"Indexed {success} docs into '{index_name}'")
        if errors:
            print(f"  Errors: {len(errors)} — first: {errors[0]}")


if __name__ == "__main__":
    ingest_all()
    print("\nDone. Verifying counts:")
    for index_name in MAPPINGS:
        if es.indices.exists(index=index_name):
            count = es.count(index=index_name)["count"]
            print(f"  {index_name}: {count} docs")
