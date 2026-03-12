"""
Excel-based data access layer.

Loads department-specific Excel files and shared patient/doctor registries.
Each department Excel has sheets: visits, medications, lab_results.
Shared files: patients.xlsx, doctors.xlsx, appointments.xlsx
"""

import pandas as pd
import logging
from pathlib import Path
from config.settings import DATA_DIR, DEPARTMENTS

logger = logging.getLogger(__name__)


class ExcelStore:
    """In-memory store backed by Excel files — one per department + shared registries."""

    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or DATA_DIR)
        self._patients = None
        self._doctors = None
        self._appointments = None
        self._departments = {}  # dept_name -> {visits, medications, lab_results}
        self._load_all()

    # ── Loading ────────────────────────────────────────────────────────────

    def _load_all(self):
        self._patients = self._read_excel("patients.xlsx")
        self._doctors = self._read_excel("doctors.xlsx")
        self._appointments = self._read_excel("appointments.xlsx")

        for dept in DEPARTMENTS:
            path = self.data_dir / f"{dept}.xlsx"
            if path.exists():
                self._departments[dept] = {
                    "visits": self._read_sheet(path, "visits"),
                    "medications": self._read_sheet(path, "medications"),
                    "lab_results": self._read_sheet(path, "lab_results"),
                }

    def _read_excel(self, filename):
        path = self.data_dir / filename
        if not path.exists():
            logger.warning(f"Data file not found: {path}")
            return pd.DataFrame()
        return pd.read_excel(path, engine="openpyxl")

    def _read_sheet(self, path, sheet):
        try:
            return pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
        except Exception:
            return pd.DataFrame()

    # ── Patient Search ─────────────────────────────────────────────────────

    def search_patients(self, fin_last4=None, name=None, phone=None, email=None, dob=None, fin_number=None):
        """
        Flexible patient search supporting multiple identifier combinations.
        Returns list of matching patient dicts.
        """
        df = self._patients.copy()
        if df.empty:
            return []

        mask = pd.Series([True] * len(df), index=df.index)

        if fin_number:
            mask &= df["fin_number"].astype(str).str.upper() == fin_number.upper()
        if fin_last4:
            mask &= df["fin_number"].astype(str).str[-5:-1] == str(fin_last4)
        if name:
            mask &= df["name"].astype(str).str.lower().str.contains(name.lower(), na=False)
        if phone:
            clean = str(phone).replace("+65", "").replace("-", "").replace(" ", "")
            mask &= df["phone"].astype(str).str.replace(r"[^\d]", "", regex=True).str.contains(clean, na=False)
        if email:
            mask &= df["email"].astype(str).str.lower() == email.lower()
        if dob:
            mask &= df["dob"].astype(str).str.contains(str(dob), na=False)

        results = df[mask]
        return results.to_dict(orient="records")

    def get_patient(self, patient_id):
        """Get a single patient by ID."""
        df = self._patients
        match = df[df["patient_id"] == patient_id]
        if match.empty:
            return None
        return match.iloc[0].to_dict()

    # ── Department Records ─────────────────────────────────────────────────

    def get_visit_history(self, patient_id, department=None):
        """Get visit history, optionally filtered by department."""
        results = []
        depts = [department] if department else list(self._departments.keys())
        for dept in depts:
            data = self._departments.get(dept, {})
            visits = data.get("visits", pd.DataFrame())
            if visits.empty:
                continue
            filtered = visits[visits["patient_id"] == patient_id]
            for _, row in filtered.iterrows():
                rec = row.to_dict()
                rec["department"] = dept
                results.append(rec)
        return sorted(results, key=lambda x: str(x.get("visit_date", "")), reverse=True)

    def get_medications(self, patient_id, department=None):
        """Get medications, optionally filtered by department."""
        results = []
        depts = [department] if department else list(self._departments.keys())
        for dept in depts:
            data = self._departments.get(dept, {})
            meds = data.get("medications", pd.DataFrame())
            if meds.empty:
                continue
            filtered = meds[meds["patient_id"] == patient_id]
            for _, row in filtered.iterrows():
                rec = row.to_dict()
                rec["department"] = dept
                results.append(rec)
        return results

    def get_lab_results(self, patient_id, department=None):
        """Get lab results, optionally filtered by department."""
        results = []
        depts = [department] if department else list(self._departments.keys())
        for dept in depts:
            data = self._departments.get(dept, {})
            labs = data.get("lab_results", pd.DataFrame())
            if labs.empty:
                continue
            filtered = labs[labs["patient_id"] == patient_id]
            for _, row in filtered.iterrows():
                rec = row.to_dict()
                rec["department"] = dept
                results.append(rec)
        return sorted(results, key=lambda x: str(x.get("test_date", "")), reverse=True)

    # ── Doctors & Appointments ─────────────────────────────────────────────

    def get_doctors(self, department=None):
        """List doctors, optionally filtered by department."""
        df = self._doctors
        if df.empty:
            return []
        if department:
            df = df[df["departments"].astype(str).str.lower().str.contains(department.lower(), na=False)]
        return df.to_dict(orient="records")

    def get_doctor(self, doctor_id):
        df = self._doctors
        match = df[df["doctor_id"] == doctor_id]
        if match.empty:
            return None
        return match.iloc[0].to_dict()

    def check_doctor_availability(self, doctor_id, date):
        """Check if a doctor has open slots on a given date."""
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            return {"available": False, "reason": "Doctor not found"}

        existing = self._appointments[
            (self._appointments["doctor_id"] == doctor_id)
            & (self._appointments["date"].astype(str) == str(date))
            & (self._appointments["status"] != "cancelled")
        ]

        available_hours = str(doctor.get("available_hours", "09:00-17:00"))
        booked_times = existing["time"].tolist() if not existing.empty else []

        # Generate 30-min slots
        start_h, end_h = 9, 17
        try:
            parts = available_hours.split("-")
            start_h = int(parts[0].split(":")[0])
            end_h = int(parts[1].split(":")[0])
        except (ValueError, IndexError):
            pass

        all_slots = [f"{h:02d}:{m:02d}" for h in range(start_h, end_h) for m in (0, 30)]
        booked_set = {str(t).strip() for t in booked_times}
        open_slots = [s for s in all_slots if s not in booked_set]

        return {
            "doctor_id": doctor_id,
            "doctor_name": doctor.get("name"),
            "date": str(date),
            "available": len(open_slots) > 0,
            "open_slots": open_slots,
            "booked_count": len(booked_set),
        }

    def book_appointment(self, patient_id, doctor_id, department, date, time, reason):
        """Book an appointment. Appends to the appointments DataFrame and saves."""
        new_appt = {
            "appointment_id": f"APT{len(self._appointments) + 1:04d}",
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "department": department,
            "date": str(date),
            "time": str(time),
            "reason": reason,
            "status": "scheduled",
        }
        self._appointments = pd.concat(
            [self._appointments, pd.DataFrame([new_appt])], ignore_index=True
        )
        self._save_appointments()
        return new_appt

    def get_appointments(self, patient_id=None, doctor_id=None, department=None):
        """Get appointments with optional filters."""
        df = self._appointments.copy()
        if df.empty:
            return []
        if patient_id:
            df = df[df["patient_id"] == patient_id]
        if doctor_id:
            df = df[df["doctor_id"] == doctor_id]
        if department:
            df = df[df["department"].astype(str).str.lower() == department.lower()]
        return df.to_dict(orient="records")

    def _save_appointments(self):
        path = self.data_dir / "appointments.xlsx"
        self._appointments.to_excel(path, index=False, engine="openpyxl")


# Singleton — initialized on first import
store = ExcelStore()
