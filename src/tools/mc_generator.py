"""
Medical Certificate (MC) generation tool.

Generates a formatted MC document when approved by a doctor.
"""

from datetime import datetime

SCHEMA = {
    "type": "function",
    "function": {
        "name": "generate_medical_certificate",
        "description": (
            "Generate a medical certificate for a patient. "
            "Requires doctor approval. Includes patient details, diagnosis, and MC duration."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
                "doctor_id": {"type": "string", "description": "Approving doctor ID"},
                "diagnosis": {"type": "string", "description": "Diagnosis / reason for MC"},
                "start_date": {"type": "string", "description": "MC start date (YYYY-MM-DD)"},
                "end_date": {"type": "string", "description": "MC end date (YYYY-MM-DD)"},
                "notes": {"type": "string", "description": "Additional notes"},
            },
            "required": ["patient_id", "doctor_id", "diagnosis", "start_date", "end_date"],
        },
    },
}


def execute(store, patient_id, doctor_id, diagnosis, start_date, end_date, notes=""):
    """Generate an MC document."""
    patient = store.get_patient(patient_id)
    if not patient:
        return {"success": False, "message": f"Patient {patient_id} not found."}

    doctor = store.get_doctor(doctor_id)
    if not doctor:
        return {"success": False, "message": f"Doctor {doctor_id} not found."}

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
    except ValueError:
        return {"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}

    mc = {
        "mc_number": f"MC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": datetime.now().isoformat(),
        "patient_name": patient["name"],
        "patient_fin": patient["fin_number"],
        "patient_dob": str(patient["dob"]),
        "doctor_name": doctor["name"],
        "doctor_specialization": doctor.get("specialization", ""),
        "diagnosis": diagnosis,
        "mc_start": start_date,
        "mc_end": end_date,
        "total_days": days,
        "notes": notes,
        "status": "PENDING_DOCTOR_APPROVAL",
    }

    mc_text = f"""
═══════════════════════════════════════════
         MEDICAL CERTIFICATE
═══════════════════════════════════════════
MC No: {mc['mc_number']}
Date:  {mc['generated_at'][:10]}

PATIENT
  Name:   {mc['patient_name']}
  FIN:    {mc['patient_fin']}
  DOB:    {mc['patient_dob']}

CERTIFYING DOCTOR
  Name:   {mc['doctor_name']}
  Dept:   {mc['doctor_specialization']}

MEDICAL LEAVE
  Diagnosis: {mc['diagnosis']}
  Period:    {mc['mc_start']} to {mc['mc_end']} ({mc['total_days']} day(s))
  Notes:     {mc['notes'] or 'Nil'}

Status: ⏳ {mc['status']}
═══════════════════════════════════════════
"""

    return {"success": True, "mc": mc, "mc_document": mc_text.strip()}
