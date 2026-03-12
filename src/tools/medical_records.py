"""
Medical records tool — visit history, medications (with expiry alerts), lab results.
"""

from datetime import datetime, date


SCHEMA_VISIT_HISTORY = {
    "type": "function",
    "function": {
        "name": "get_visit_history",
        "description": "Get a patient's hospital visit history across all or a specific department.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "department": {"type": "string", "description": "Optional: filter by department"},
            },
            "required": ["patient_id"],
        },
    },
}

SCHEMA_MEDICATIONS = {
    "type": "function",
    "function": {
        "name": "get_medications",
        "description": (
            "Get a patient's current and past medications. "
            "Flags medications that are expiring before the next appointment."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "department": {"type": "string", "description": "Optional: filter by department"},
            },
            "required": ["patient_id"],
        },
    },
}

SCHEMA_LAB_RESULTS = {
    "type": "function",
    "function": {
        "name": "get_lab_results",
        "description": "Get a patient's lab test results across departments.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "department": {"type": "string", "description": "Optional: filter by department"},
            },
            "required": ["patient_id"],
        },
    },
}

SCHEMA_PATIENT_SUMMARY = {
    "type": "function",
    "function": {
        "name": "get_patient_summary",
        "description": (
            "Get a comprehensive summary for a patient: demographics, allergies, "
            "visit history, current medications (with expiry warnings), upcoming appointments, "
            "and recent lab results."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
            },
            "required": ["patient_id"],
        },
    },
}


def _check_med_expiry(meds, appointments):
    """Flag medications that will run out before the next scheduled appointment."""
    today = date.today()

    # Find the patient's next appointment date
    upcoming = []
    for appt in appointments:
        try:
            appt_date = datetime.strptime(str(appt.get("date", ""))[:10], "%Y-%m-%d").date()
            if appt_date >= today:
                upcoming.append(appt_date)
        except (ValueError, TypeError):
            continue
    next_appt = min(upcoming) if upcoming else None

    for med in meds:
        try:
            end = datetime.strptime(str(med.get("end_date", ""))[:10], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            end = None

        med["is_expired"] = end is not None and end <= today
        med["refills_remaining"] = med.get("refills_remaining", 0)

        if next_appt and end:
            if end < next_appt and med.get("refills_remaining", 0) == 0:
                med["warning"] = f"⚠️ Medication expires {end} BEFORE next appointment on {next_appt}. No refills remaining."
            elif end < next_appt:
                med["warning"] = f"Medication expires {end} before next appointment ({next_appt}), but {med['refills_remaining']} refill(s) available."

    return meds


def get_visit_history(store, patient_id, department=None):
    visits = store.get_visit_history(patient_id, department=department)
    return {"patient_id": patient_id, "count": len(visits), "visits": visits}


def get_medications(store, patient_id, department=None):
    meds = store.get_medications(patient_id, department=department)
    appointments = store.get_appointments(patient_id=patient_id)
    meds = _check_med_expiry(meds, appointments)

    active = [m for m in meds if not m.get("is_expired")]
    expired = [m for m in meds if m.get("is_expired")]
    warnings = [m for m in meds if m.get("warning")]

    return {
        "patient_id": patient_id,
        "active_medications": active,
        "expired_medications": expired,
        "medication_warnings": [m["warning"] for m in warnings],
        "total": len(meds),
    }


def get_lab_results(store, patient_id, department=None):
    labs = store.get_lab_results(patient_id, department=department)
    return {"patient_id": patient_id, "count": len(labs), "results": labs}


def get_patient_summary(store, patient_id):
    patient = store.get_patient(patient_id)
    if not patient:
        return {"found": False, "message": f"Patient {patient_id} not found."}

    visits = store.get_visit_history(patient_id)
    meds = store.get_medications(patient_id)
    appointments = store.get_appointments(patient_id=patient_id)
    meds = _check_med_expiry(meds, appointments)
    labs = store.get_lab_results(patient_id)

    return {
        "found": True,
        "patient": patient,
        "visit_count": len(visits),
        "recent_visits": visits[:5],
        "active_medications": [m for m in meds if not m.get("is_expired")],
        "medication_warnings": [m["warning"] for m in meds if m.get("warning")],
        "upcoming_appointments": [a for a in appointments if str(a.get("status")) == "scheduled"],
        "recent_labs": labs[:5],
    }
