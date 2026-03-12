"""
Triage sub-agent — classifies urgency and routes to the right department.

Uses LLM reasoning over patient symptoms + history to determine:
  - Emergency vs Urgent vs Routine
  - Target department
"""

from src.agents.base import BaseAgent
from src.tools import patient_search, medical_records
from src.db.excel_store import ExcelStore


TRIAGE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_patient_history_for_triage",
        "description": "Retrieve patient's medical history to assist with triage decision.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Patient ID"},
            },
            "required": ["patient_id"],
        },
    },
}


class TriageAgent(BaseAgent):
    """Agent that classifies urgency and routes patients to departments."""

    name = "triage_agent"

    def __init__(self, store: ExcelStore, model=None):
        super().__init__(model=model)
        self._store = store

        self.system_prompt = """You are the triage and routing assistant for MediGuard Hospital.

Your job is to:
1. Assess the urgency of a patient's condition based on described symptoms
2. Route them to the appropriate department
3. If the patient has existing records, factor in their medical history

URGENCY LEVELS:
- 🚨 EMERGENCY: Life-threatening conditions requiring immediate attention
  Examples: chest pain with cardiac history, severe breathing difficulty, stroke symptoms,
  anaphylaxis, major trauma, loss of consciousness
- ⚡ URGENT: Needs same-day attention but not immediately life-threatening
  Examples: high fever 3+ days, severe pain, diabetic with unusual symptoms,
  sudden vision changes, moderate injuries
- 📋 ROUTINE: Can be scheduled for a regular appointment
  Examples: annual checkup, chronic condition follow-up, minor aches,
  medication refills, screening tests

DEPARTMENTS:
- emergency: For all emergency-level cases
- cardiology: Heart-related conditions
- orthopedics: Bone, joint, muscle issues
- neurology: Brain, nerve, seizure conditions
- oncology: Cancer-related care
- general_medicine: Everything else, initial evaluations, chronic disease management

Always provide:
1. Urgency level (EMERGENCY / URGENT / ROUTINE)
2. Recommended department
3. Brief reasoning
4. Any flags based on patient history (allergies, current medications, etc.)"""

        self._register_tools()

    def _register_tools(self):
        self.tool_schemas.append(patient_search.SCHEMA)
        self.tool_handlers["search_patient"] = lambda **kw: patient_search.execute(self._store, **kw)

        self.tool_schemas.append(TRIAGE_SCHEMA)
        self.tool_handlers["get_patient_history_for_triage"] = self._get_history

        self.tool_schemas.append(medical_records.SCHEMA_PATIENT_SUMMARY)
        self.tool_handlers["get_patient_summary"] = lambda **kw: medical_records.get_patient_summary(self._store, **kw)

    def _get_history(self, patient_id):
        patient = self._store.get_patient(patient_id)
        if not patient:
            return {"found": False}
        visits = self._store.get_visit_history(patient_id)
        meds = self._store.get_medications(patient_id)
        return {
            "found": True,
            "patient": patient,
            "allergies": patient.get("allergies", "None"),
            "recent_visits": visits[:5],
            "current_medications": [m["drug_name"] for m in meds],
        }
