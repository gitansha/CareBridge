"""
Patient search tool — flexible multi-identifier lookup across the patient registry.
"""

import json

SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_patient",
        "description": (
            "Search for a patient using any combination of: last 4 digits of FIN, "
            "full FIN number, name, phone number, email, or date of birth. "
            "Returns matching patient records with demographics and allergy info."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "fin_last4": {
                    "type": "string",
                    "description": "Last 4 digits of the FIN number (e.g. '2345')",
                },
                "fin_number": {
                    "type": "string",
                    "description": "Full FIN/NRIC number (e.g. 'S9012345A')",
                },
                "name": {
                    "type": "string",
                    "description": "Patient name or partial name",
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number (any format)",
                },
                "email": {
                    "type": "string",
                    "description": "Email address",
                },
                "dob": {
                    "type": "string",
                    "description": "Date of birth (YYYY-MM-DD)",
                },
            },
            "required": [],
        },
    },
}


def execute(store, **kwargs):
    """Run patient search against the Excel store."""
    results = store.search_patients(**kwargs)
    if not results:
        return {"found": False, "count": 0, "patients": [], "message": "No patients found matching the criteria."}
    return {"found": True, "count": len(results), "patients": results}
