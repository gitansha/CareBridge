"""
Department sub-agent — one instance per department.

Each department agent can search patients within its scope, view visit history,
medications, lab results, and manage appointments for that department.
"""

from src.agents.base import BaseAgent
from src.tools import patient_search, appointment, medical_records
from src.db.excel_store import ExcelStore


class DepartmentAgent(BaseAgent):
    """Agent scoped to a single department's data."""

    def __init__(self, department, store: ExcelStore, model=None):
        super().__init__(model=model)
        self.name = f"dept_{department}"
        self.department = department

        self.system_prompt = f"""You are the {department.replace('_', ' ').title()} department assistant at MediGuard Hospital.

Your responsibilities:
- Search for patients and retrieve their records within the {department} department
- View visit history, medications, and lab results for this department
- Check doctor availability and manage appointments in this department
- Flag any medication warnings (expiring before next appointment, low refills)
- Identify urgent clinical findings in lab results

Always be precise with medical information. When showing patient data, highlight:
1. Any medication warnings or expiring prescriptions
2. Abnormal lab results
3. Upcoming follow-up dates
4. Allergy information relevant to this department

Format your responses clearly for a hospital receptionist."""

        self._store = store
        self._register_tools()

    def _register_tools(self):
        dept = self.department

        # Patient search
        self.tool_schemas.append(patient_search.SCHEMA)
        self.tool_handlers["search_patient"] = lambda **kw: patient_search.execute(self._store, **kw)

        # Visit history (scoped to department)
        self.tool_schemas.append(medical_records.SCHEMA_VISIT_HISTORY)
        self.tool_handlers["get_visit_history"] = lambda **kw: medical_records.get_visit_history(
            self._store, department=kw.pop("department", dept), **kw
        )

        # Medications (scoped to department)
        self.tool_schemas.append(medical_records.SCHEMA_MEDICATIONS)
        self.tool_handlers["get_medications"] = lambda **kw: medical_records.get_medications(
            self._store, department=kw.pop("department", dept), **kw
        )

        # Lab results (scoped to department)
        self.tool_schemas.append(medical_records.SCHEMA_LAB_RESULTS)
        self.tool_handlers["get_lab_results"] = lambda **kw: medical_records.get_lab_results(
            self._store, department=kw.pop("department", dept), **kw
        )

        # Doctor list for this department
        self.tool_schemas.append(appointment.SCHEMA_LIST_DOCTORS)
        self.tool_handlers["list_doctors"] = lambda **kw: appointment.list_doctors(
            self._store, department=kw.pop("department", dept)
        )

        # Appointments
        self.tool_schemas.append(appointment.SCHEMA_CHECK_AVAILABILITY)
        self.tool_handlers["check_doctor_availability"] = lambda **kw: appointment.check_availability(self._store, **kw)

        self.tool_schemas.append(appointment.SCHEMA_BOOK)
        self.tool_handlers["book_appointment"] = lambda **kw: appointment.book(self._store, **kw)

        self.tool_schemas.append(appointment.SCHEMA_VIEW)
        self.tool_handlers["view_appointments"] = lambda **kw: appointment.view(
            self._store, department=kw.pop("department", dept), **kw
        )
