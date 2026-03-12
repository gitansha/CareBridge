"""
Orchestrator (aggregator) agent — the top-level coordinator.

Receives receptionist queries and dispatches to the correct sub-agents:
  - Department agents (one per department)
  - Drug interaction agent
  - ICD-10 classification agent
  - Triage agent

The orchestrator itself has meta-tools that invoke sub-agents and cross-
department queries.
"""

import json
import logging
from src.agents.base import BaseAgent
from src.agents.department_agent import DepartmentAgent
from src.agents.drug_agent import DrugAgent
from src.agents.icd_agent import ICDAgent
from src.agents.triage_agent import TriageAgent
from src.tools import patient_search, medical_records, appointment, mc_generator
from src.db.excel_store import ExcelStore
from config.settings import DEPARTMENTS

logger = logging.getLogger(__name__)


class Orchestrator(BaseAgent):
    """
    Top-level agent that coordinates sub-agents.

    Has direct tools for cross-department operations and meta-tools
    that dispatch queries to specialized sub-agents.
    """

    name = "orchestrator"

    def __init__(self, store: ExcelStore = None, model=None):
        super().__init__(model=model)

        self._store = store or ExcelStore()

        # Initialize sub-agents
        self._dept_agents = {
            dept: DepartmentAgent(dept, self._store, model=model)
            for dept in DEPARTMENTS
        }
        self._drug_agent = DrugAgent(model=model)
        self._icd_agent = ICDAgent(model=model)
        self._triage_agent = TriageAgent(self._store, model=model)

        self.system_prompt = """You are MediGuard AI, the intelligent hospital reception assistant.

You help hospital receptionists with:
1. **Patient Search**: Find patients by FIN (last 4 digits), name, phone, email, DOB, or combinations
2. **Record Navigation**: Pull visit history, medications, lab results across ALL departments
3. **Appointments**: Check doctor availability and book appointments
4. **Medication Alerts**: Flag expiring medications and check drug interactions
5. **ICD Coding**: Look up correct ICD-10/11 codes for diagnoses
6. **Triage**: Classify urgency and route to the right department
7. **Medical Certificates**: Generate MCs when approved by a doctor

WORKFLOW GUIDELINES:
- When a patient is identified, proactively show their summary (allergies, upcoming appointments, medication warnings)
- If a patient doesn't exist, help check doctor availability and book a new appointment
- For medication queries, always check for drug interactions if multiple drugs are involved
- When routing patients, use the triage agent for symptom-based decisions
- Cross-reference multiple departments when a patient has visits in several areas
- Flag medications running out before the next scheduled appointment

IMPORTANT:
- Always verify patient identity before sharing records
- Be concise but thorough — receptionists are busy
- Highlight critical information (allergies, warnings) prominently
- Format responses for easy scanning

You have access to tools for searching patients, viewing records across departments,
managing appointments, checking drug interactions, looking up ICD codes, triaging
patients, and generating medical certificates."""

        self._register_tools()

    def _register_tools(self):
        # ── Cross-department patient tools ──────────────────────────────

        self.tool_schemas.append(patient_search.SCHEMA)
        self.tool_handlers["search_patient"] = lambda **kw: patient_search.execute(self._store, **kw)

        self.tool_schemas.append(medical_records.SCHEMA_PATIENT_SUMMARY)
        self.tool_handlers["get_patient_summary"] = lambda **kw: medical_records.get_patient_summary(self._store, **kw)

        self.tool_schemas.append(medical_records.SCHEMA_VISIT_HISTORY)
        self.tool_handlers["get_visit_history"] = lambda **kw: medical_records.get_visit_history(self._store, **kw)

        self.tool_schemas.append(medical_records.SCHEMA_MEDICATIONS)
        self.tool_handlers["get_medications"] = lambda **kw: medical_records.get_medications(self._store, **kw)

        self.tool_schemas.append(medical_records.SCHEMA_LAB_RESULTS)
        self.tool_handlers["get_lab_results"] = lambda **kw: medical_records.get_lab_results(self._store, **kw)

        # ── Appointment tools ───────────────────────────────────────────

        self.tool_schemas.append(appointment.SCHEMA_LIST_DOCTORS)
        self.tool_handlers["list_doctors"] = lambda **kw: appointment.list_doctors(self._store, **kw)

        self.tool_schemas.append(appointment.SCHEMA_CHECK_AVAILABILITY)
        self.tool_handlers["check_doctor_availability"] = lambda **kw: appointment.check_availability(self._store, **kw)

        self.tool_schemas.append(appointment.SCHEMA_BOOK)
        self.tool_handlers["book_appointment"] = lambda **kw: appointment.book(self._store, **kw)

        self.tool_schemas.append(appointment.SCHEMA_VIEW)
        self.tool_handlers["view_appointments"] = lambda **kw: appointment.view(self._store, **kw)

        # ── Drug interaction tools ──────────────────────────────────────

        self.tool_schemas.append({
            "type": "function",
            "function": {
                "name": "check_drug_interactions",
                "description": (
                    "Check for drug-drug interactions between medications. "
                    "Use this when a patient is on multiple drugs or before prescribing new ones."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "drug_list": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of drug names to check for interactions",
                        },
                    },
                    "required": ["drug_list"],
                },
            },
        })
        self.tool_handlers["check_drug_interactions"] = self._dispatch_drug_interaction

        self.tool_schemas.append({
            "type": "function",
            "function": {
                "name": "get_drug_info",
                "description": "Get detailed drug label info (warnings, contraindications, interactions).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "drug_name": {"type": "string", "description": "Generic drug name"},
                    },
                    "required": ["drug_name"],
                },
            },
        })
        self.tool_handlers["get_drug_info"] = self._dispatch_drug_info

        # ── ICD coding tools ───────────────────────────────────────────

        self.tool_schemas.append({
            "type": "function",
            "function": {
                "name": "search_icd_code",
                "description": "Search for ICD-10/11 code by diagnosis description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Diagnosis description"},
                        "version": {"type": "string", "enum": ["icd10", "icd11"], "description": "ICD version (default: icd10)"},
                    },
                    "required": ["query"],
                },
            },
        })
        self.tool_handlers["search_icd_code"] = self._dispatch_icd_search

        # ── Triage tool ─────────────────────────────────────────────────

        self.tool_schemas.append({
            "type": "function",
            "function": {
                "name": "triage_patient",
                "description": (
                    "Assess urgency and route a patient to the correct department based on symptoms. "
                    "Provide the symptoms and optionally a patient ID for history context."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symptoms": {"type": "string", "description": "Description of symptoms/complaint"},
                        "patient_id": {"type": "string", "description": "Patient ID (optional, for history context)"},
                    },
                    "required": ["symptoms"],
                },
            },
        })
        self.tool_handlers["triage_patient"] = self._dispatch_triage

        # ── MC generation ───────────────────────────────────────────────

        self.tool_schemas.append(mc_generator.SCHEMA)
        self.tool_handlers["generate_medical_certificate"] = lambda **kw: mc_generator.execute(self._store, **kw)

        # ── Department-specific query ───────────────────────────────────

        self.tool_schemas.append({
            "type": "function",
            "function": {
                "name": "query_department",
                "description": (
                    "Send a specific query to a department sub-agent for detailed, "
                    "department-scoped information."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "enum": DEPARTMENTS,
                            "description": "Target department",
                        },
                        "query": {"type": "string", "description": "The query to ask the department agent"},
                    },
                    "required": ["department", "query"],
                },
            },
        })
        self.tool_handlers["query_department"] = self._dispatch_department

    # ── Dispatch methods ────────────────────────────────────────────────

    def _dispatch_department(self, department, query):
        agent = self._dept_agents.get(department)
        if not agent:
            return {"error": f"Unknown department: {department}"}
        try:
            result = agent.run(query)
            return {"department": department, "response": result}
        except Exception as e:
            logger.error(f"Department agent error ({department}): {e}")
            return {"error": str(e)}

    def _dispatch_drug_interaction(self, drug_list):
        from src.tools.drug_api import check_drug_interactions
        return check_drug_interactions(drug_list)

    def _dispatch_drug_info(self, drug_name):
        from src.tools.drug_api import get_drug_info
        return get_drug_info(drug_name)

    def _dispatch_icd_search(self, query, version="icd10"):
        from src.tools.icd_api import search_icd_code
        return search_icd_code(query, version)

    def _dispatch_triage(self, symptoms, patient_id=None):
        query = f"Patient symptoms: {symptoms}"
        context = None
        if patient_id:
            summary = medical_records.get_patient_summary(self._store, patient_id)
            if summary.get("found"):
                context = json.dumps(summary, default=str)
        try:
            result = self._triage_agent.run(query, context=context)
            return {"triage_result": result}
        except Exception as e:
            logger.error(f"Triage agent error: {e}")
            return {"error": str(e)}
