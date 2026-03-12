"""
Appointment tool — check doctor availability, book and view appointments.
"""

SCHEMA_CHECK_AVAILABILITY = {
    "type": "function",
    "function": {
        "name": "check_doctor_availability",
        "description": "Check a doctor's available time slots on a given date.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_id": {"type": "string", "description": "Doctor ID (e.g. 'D001')"},
                "date": {"type": "string", "description": "Date to check (YYYY-MM-DD)"},
            },
            "required": ["doctor_id", "date"],
        },
    },
}

SCHEMA_BOOK = {
    "type": "function",
    "function": {
        "name": "book_appointment",
        "description": "Book an appointment for a patient with a specific doctor.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "doctor_id": {"type": "string", "description": "Doctor ID"},
                "department": {"type": "string", "description": "Department name"},
                "date": {"type": "string", "description": "Appointment date (YYYY-MM-DD)"},
                "time": {"type": "string", "description": "Appointment time (HH:MM)"},
                "reason": {"type": "string", "description": "Reason for appointment"},
            },
            "required": ["patient_id", "doctor_id", "department", "date", "time", "reason"],
        },
    },
}

SCHEMA_VIEW = {
    "type": "function",
    "function": {
        "name": "view_appointments",
        "description": "View upcoming/past appointments for a patient, doctor, or department.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "doctor_id": {"type": "string", "description": "Doctor ID"},
                "department": {"type": "string", "description": "Department name"},
            },
            "required": [],
        },
    },
}

SCHEMA_LIST_DOCTORS = {
    "type": "function",
    "function": {
        "name": "list_doctors",
        "description": "List doctors, optionally filtered by department.",
        "parameters": {
            "type": "object",
            "properties": {
                "department": {"type": "string", "description": "Filter by department name"},
            },
            "required": [],
        },
    },
}


def check_availability(store, doctor_id, date):
    return store.check_doctor_availability(doctor_id, date)


def book(store, patient_id, doctor_id, department, date, time, reason):
    # Verify slot is open
    avail = store.check_doctor_availability(doctor_id, date)
    if not avail["available"]:
        return {"success": False, "message": "No available slots on that date."}
    if time not in avail["open_slots"]:
        return {"success": False, "message": f"Time {time} is not available. Open slots: {avail['open_slots'][:5]}"}

    appt = store.book_appointment(patient_id, doctor_id, department, date, time, reason)
    return {"success": True, "appointment": appt}


def view(store, patient_id=None, doctor_id=None, department=None):
    results = store.get_appointments(patient_id=patient_id, doctor_id=doctor_id, department=department)
    return {"count": len(results), "appointments": results}


def list_doctors(store, department=None):
    docs = store.get_doctors(department=department)
    return {"count": len(docs), "doctors": docs}
