#!/usr/bin/env python3
"""
Generate sample Excel datasets for MediGuard AI.

Run once:  python -m data.seed_data
Produces:  data/patients.xlsx, data/doctors.xlsx, data/appointments.xlsx,
           data/<department>.xlsx  (one per department)
"""

import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import random

DATA_DIR = Path(__file__).resolve().parent
random.seed(42)

# ── Patients ────────────────────────────────────────────────────────────────

PATIENTS = [
    {"patient_id": "P001", "fin_number": "S9012345A", "name": "Tan Wei Ming", "phone": "+65-9123-4567", "email": "weiming.tan@email.com", "dob": "1990-03-15", "blood_type": "O+", "allergies": "Penicillin", "emergency_contact": "Tan Mei Li (+65-8234-5678)"},
    {"patient_id": "P002", "fin_number": "S5523456B", "name": "Lim Ah Hua", "phone": "+65-8234-5678", "email": "ahhua.lim@email.com", "dob": "1955-08-22", "blood_type": "A+", "allergies": "Sulfa drugs", "emergency_contact": "Lim Wei Jie (+65-9345-6789)"},
    {"patient_id": "P003", "fin_number": "S8834567C", "name": "Priya Devi", "phone": "+65-9345-6789", "email": "priya.devi@email.com", "dob": "1988-11-01", "blood_type": "B+", "allergies": "None", "emergency_contact": "Raj Devi (+65-8456-7890)"},
    {"patient_id": "P004", "fin_number": "S7745678D", "name": "Muhammad Farhan", "phone": "+65-8456-7890", "email": "farhan.m@email.com", "dob": "1977-04-10", "blood_type": "AB+", "allergies": "Latex", "emergency_contact": "Siti Farhan (+65-9567-8901)"},
    {"patient_id": "P005", "fin_number": "S6656789E", "name": "Chen Xiao Li", "phone": "+65-9567-8901", "email": "xiaoli.chen@email.com", "dob": "1966-07-30", "blood_type": "A-", "allergies": "Aspirin", "emergency_contact": "Chen Wei (+65-8678-9012)"},
    {"patient_id": "P006", "fin_number": "S8567890F", "name": "Siti Aminah", "phone": "+65-8678-9012", "email": "aminah.siti@email.com", "dob": "1985-12-05", "blood_type": "O+", "allergies": "None", "emergency_contact": "Ahmad Bin Ali (+65-9789-0123)"},
    {"patient_id": "P007", "fin_number": "S7078901G", "name": "Raj Kumar", "phone": "+65-9789-0123", "email": "raj.kumar@email.com", "dob": "1970-02-18", "blood_type": "B-", "allergies": "Iodine", "emergency_contact": "Priya Kumar (+65-8890-1234)"},
    {"patient_id": "P008", "fin_number": "S8589012H", "name": "Wong Mei Ling", "phone": "+65-8890-1234", "email": "meiling.wong@email.com", "dob": "1985-09-25", "blood_type": "O-", "allergies": "Codeine", "emergency_contact": "Wong Ah Kow (+65-9901-2345)"},
    {"patient_id": "P009", "fin_number": "S6090123I", "name": "Ahmad Bin Hassan", "phone": "+65-9901-2345", "email": "ahmad.hassan@email.com", "dob": "1960-06-12", "blood_type": "A+", "allergies": "None", "emergency_contact": "Hassan Bin Ali (+65-8012-3456)"},
    {"patient_id": "P010", "fin_number": "F2501234J", "name": "Tanaka Yuki", "phone": "+65-8012-3456", "email": "yuki.tanaka@email.com", "dob": "1995-01-08", "blood_type": "AB-", "allergies": "None", "emergency_contact": "Tanaka Hiro (+65-9123-4568)"},
    {"patient_id": "P011", "fin_number": "S5512345K", "name": "Lee Siew Lan", "phone": "+65-9213-4567", "email": "siewlan.lee@email.com", "dob": "1955-05-20", "blood_type": "B+", "allergies": "Morphine", "emergency_contact": "Lee Ah Beng (+65-8324-5679)"},
    {"patient_id": "P012", "fin_number": "S7023456L", "name": "Ng Boon Teck", "phone": "+65-8324-5679", "email": "boonteck.ng@email.com", "dob": "1970-10-14", "blood_type": "O+", "allergies": "None", "emergency_contact": "Ng Mei Hua (+65-9435-6780)"},
    {"patient_id": "P013", "fin_number": "S8534567M", "name": "Fatimah Zahra", "phone": "+65-9435-6780", "email": "fatimah.z@email.com", "dob": "1985-03-28", "blood_type": "A-", "allergies": "Shellfish", "emergency_contact": "Zahra Ali (+65-8546-7891)"},
    {"patient_id": "P014", "fin_number": "S9045678N", "name": "David Lim", "phone": "+65-8546-7891", "email": "david.lim@email.com", "dob": "1990-08-03", "blood_type": "AB+", "allergies": "None", "emergency_contact": "Sarah Lim (+65-9657-8902)"},
    {"patient_id": "P015", "fin_number": "S6556789O", "name": "Aisha Begum", "phone": "+65-9657-8902", "email": "aisha.begum@email.com", "dob": "1965-11-17", "blood_type": "B+", "allergies": "ACE inhibitors", "emergency_contact": "Begum Ali (+65-8768-9013)"},
    {"patient_id": "P016", "fin_number": "S7567890P", "name": "Chong Kok Wei", "phone": "+65-8768-9013", "email": "kokwei.chong@email.com", "dob": "1975-06-22", "blood_type": "O+", "allergies": "None", "emergency_contact": "Chong Ah Mei (+65-9879-0124)"},
    {"patient_id": "P017", "fin_number": "S8078901Q", "name": "Suresh Nair", "phone": "+65-9879-0124", "email": "suresh.nair@email.com", "dob": "1980-01-09", "blood_type": "A+", "allergies": "Contrast dye", "emergency_contact": "Nair Lakshmi (+65-8980-1235)"},
    {"patient_id": "P018", "fin_number": "S9089012R", "name": "Goh Hui Min", "phone": "+65-8980-1235", "email": "huimin.goh@email.com", "dob": "1990-04-14", "blood_type": "B-", "allergies": "Bee stings, Peanuts", "emergency_contact": "Goh Ah Seng (+65-9091-2346)"},
    {"patient_id": "P019", "fin_number": "S6590123S", "name": "Halimah Yusof", "phone": "+65-9091-2346", "email": "halimah.y@email.com", "dob": "1965-09-30", "blood_type": "O-", "allergies": "NSAIDs", "emergency_contact": "Yusof Ahmad (+65-8102-3457)"},
    {"patient_id": "P020", "fin_number": "S8501234T", "name": "Jason Teo", "phone": "+65-8102-3457", "email": "jason.teo@email.com", "dob": "1985-07-07", "blood_type": "AB+", "allergies": "None", "emergency_contact": "Teo Mei (+65-9213-4569)"},
]

# ── Doctors ─────────────────────────────────────────────────────────────────

DOCTORS = [
    {"doctor_id": "D001", "name": "Dr. Tan Beng Choo", "departments": "cardiology", "specialization": "Interventional Cardiology", "available_days": "Mon,Tue,Wed,Thu,Fri", "available_hours": "09:00-17:00", "room": "C-201"},
    {"doctor_id": "D002", "name": "Dr. Lee Wei Xiang", "departments": "cardiology,emergency", "specialization": "Cardiac Emergency", "available_days": "Mon,Wed,Fri", "available_hours": "08:00-16:00", "room": "C-202"},
    {"doctor_id": "D003", "name": "Dr. Srinivasan Raghavan", "departments": "orthopedics", "specialization": "Joint Replacement", "available_days": "Mon,Tue,Thu,Fri", "available_hours": "09:00-17:00", "room": "O-101"},
    {"doctor_id": "D004", "name": "Dr. Aishah Binte Omar", "departments": "orthopedics,general_medicine", "specialization": "Sports Medicine", "available_days": "Tue,Wed,Thu", "available_hours": "09:00-17:00", "room": "O-102"},
    {"doctor_id": "D005", "name": "Dr. Lim Kok Ping", "departments": "general_medicine", "specialization": "Internal Medicine", "available_days": "Mon,Tue,Wed,Thu,Fri", "available_hours": "08:30-17:30", "room": "G-301"},
    {"doctor_id": "D006", "name": "Dr. Chen Yi Wen", "departments": "general_medicine", "specialization": "Family Medicine", "available_days": "Mon,Wed,Fri", "available_hours": "09:00-17:00", "room": "G-302"},
    {"doctor_id": "D007", "name": "Dr. Patel Nirav", "departments": "neurology", "specialization": "Epilepsy & Seizure Disorders", "available_days": "Mon,Tue,Wed,Thu", "available_hours": "09:00-17:00", "room": "N-401"},
    {"doctor_id": "D008", "name": "Dr. Fatima Hassan", "departments": "neurology,emergency", "specialization": "Neurocritical Care", "available_days": "Tue,Thu,Fri", "available_hours": "08:00-18:00", "room": "N-402"},
    {"doctor_id": "D009", "name": "Dr. Wong Jing Yi", "departments": "oncology", "specialization": "Medical Oncology", "available_days": "Mon,Tue,Wed,Thu,Fri", "available_hours": "09:00-17:00", "room": "ON-501"},
    {"doctor_id": "D010", "name": "Dr. Ahmad Rizwan", "departments": "oncology", "specialization": "Radiation Oncology", "available_days": "Mon,Wed,Fri", "available_hours": "09:00-16:00", "room": "ON-502"},
    {"doctor_id": "D011", "name": "Dr. Sarah Tan", "departments": "emergency", "specialization": "Emergency Medicine", "available_days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "available_hours": "00:00-23:59", "room": "ER-01"},
    {"doctor_id": "D012", "name": "Dr. Ravi Shankar", "departments": "emergency,general_medicine", "specialization": "Acute Medicine", "available_days": "Mon,Wed,Fri,Sat", "available_hours": "08:00-20:00", "room": "ER-02"},
    {"doctor_id": "D013", "name": "Dr. Chua Mei Hua", "departments": "general_medicine,cardiology", "specialization": "Preventive Cardiology", "available_days": "Tue,Thu", "available_hours": "09:00-17:00", "room": "G-303"},
    {"doctor_id": "D014", "name": "Dr. Mohamed Faiz", "departments": "orthopedics", "specialization": "Spine Surgery", "available_days": "Mon,Tue,Wed,Thu", "available_hours": "09:00-17:00", "room": "O-103"},
    {"doctor_id": "D015", "name": "Dr. Jennifer Koh", "departments": "neurology,oncology", "specialization": "Neuro-Oncology", "available_days": "Mon,Wed,Fri", "available_hours": "09:00-17:00", "room": "N-403"},
]

# ── Helper ──────────────────────────────────────────────────────────────────

today = date(2026, 3, 12)


def d(offset_days):
    """Date relative to today."""
    return str(today + timedelta(days=offset_days))


# ── Department Data ─────────────────────────────────────────────────────────

def build_cardiology():
    visits = pd.DataFrame([
        {"visit_id": "VC001", "patient_id": "P001", "doctor_id": "D001", "visit_date": d(-90), "chief_complaint": "Chest tightness during exercise", "diagnosis": "Stable angina pectoris", "icd_code": "I20.8", "notes": "Stress test ordered. Started on medication.", "follow_up_date": d(14)},
        {"visit_id": "VC002", "patient_id": "P001", "doctor_id": "D001", "visit_date": d(-30), "chief_complaint": "Follow-up for angina", "diagnosis": "Stable angina - improving", "icd_code": "I20.8", "notes": "Medication working well. Continue current regimen.", "follow_up_date": d(30)},
        {"visit_id": "VC003", "patient_id": "P002", "doctor_id": "D002", "visit_date": d(-180), "chief_complaint": "History of myocardial infarction", "diagnosis": "Old myocardial infarction", "icd_code": "I25.2", "notes": "Post-MI management. On dual antiplatelet therapy.", "follow_up_date": d(-90)},
        {"visit_id": "VC004", "patient_id": "P002", "doctor_id": "D001", "visit_date": d(-60), "chief_complaint": "Routine cardiac follow-up", "diagnosis": "Chronic ischemic heart disease", "icd_code": "I25.9", "notes": "Echo shows EF 45%. Continue medications.", "follow_up_date": d(5)},
        {"visit_id": "VC005", "patient_id": "P007", "doctor_id": "D013", "visit_date": d(-45), "chief_complaint": "High blood pressure readings at home", "diagnosis": "Essential hypertension", "icd_code": "I10", "notes": "BP 160/95. Started on Amlodipine 5mg.", "follow_up_date": d(15)},
        {"visit_id": "VC006", "patient_id": "P015", "doctor_id": "D001", "visit_date": d(-120), "chief_complaint": "Palpitations and dizziness", "diagnosis": "Atrial fibrillation", "icd_code": "I48.91", "notes": "Started on Warfarin. INR monitoring needed.", "follow_up_date": d(-30)},
        {"visit_id": "VC007", "patient_id": "P015", "doctor_id": "D001", "visit_date": d(-30), "chief_complaint": "Warfarin follow-up", "diagnosis": "Atrial fibrillation on anticoagulation", "icd_code": "I48.91", "notes": "INR stable at 2.3. Continue Warfarin 5mg.", "follow_up_date": d(30)},
        {"visit_id": "VC008", "patient_id": "P020", "doctor_id": "D002", "visit_date": d(-14), "chief_complaint": "Recurring chest pain at rest", "diagnosis": "Unstable angina", "icd_code": "I20.0", "notes": "Admitted for observation. Angiogram scheduled.", "follow_up_date": d(7)},
        {"visit_id": "VC009", "patient_id": "P011", "doctor_id": "D013", "visit_date": d(-60), "chief_complaint": "Cardiac monitoring during chemo", "diagnosis": "Chemotherapy-induced cardiomyopathy screening", "icd_code": "I42.7", "notes": "Echo baseline normal. Monitor every 3 months.", "follow_up_date": d(30)},
    ])

    medications = pd.DataFrame([
        {"med_id": "MC001", "patient_id": "P001", "visit_id": "VC001", "drug_name": "Atorvastatin", "rxcui": "83367", "dosage": "40mg", "frequency": "Once daily", "start_date": d(-90), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D001"},
        {"med_id": "MC002", "patient_id": "P001", "visit_id": "VC001", "drug_name": "Aspirin", "rxcui": "1191", "dosage": "100mg", "frequency": "Once daily", "start_date": d(-90), "end_date": d(90), "refills_remaining": 2, "prescribing_doctor": "D001"},
        {"med_id": "MC003", "patient_id": "P001", "visit_id": "VC001", "drug_name": "Metoprolol", "rxcui": "6918", "dosage": "50mg", "frequency": "Twice daily", "start_date": d(-90), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D001"},
        {"med_id": "MC004", "patient_id": "P002", "visit_id": "VC003", "drug_name": "Clopidogrel", "rxcui": "32968", "dosage": "75mg", "frequency": "Once daily", "start_date": d(-180), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D002"},
        {"med_id": "MC005", "patient_id": "P002", "visit_id": "VC003", "drug_name": "Aspirin", "rxcui": "1191", "dosage": "100mg", "frequency": "Once daily", "start_date": d(-180), "end_date": d(30), "refills_remaining": 1, "prescribing_doctor": "D002"},
        {"med_id": "MC006", "patient_id": "P015", "visit_id": "VC006", "drug_name": "Warfarin", "rxcui": "11289", "dosage": "5mg", "frequency": "Once daily", "start_date": d(-120), "end_date": d(5), "refills_remaining": 0, "prescribing_doctor": "D001"},
        {"med_id": "MC007", "patient_id": "P007", "visit_id": "VC005", "drug_name": "Amlodipine", "rxcui": "17767", "dosage": "5mg", "frequency": "Once daily", "start_date": d(-45), "end_date": d(45), "refills_remaining": 1, "prescribing_doctor": "D013"},
        {"med_id": "MC008", "patient_id": "P020", "visit_id": "VC008", "drug_name": "Nitroglycerin", "rxcui": "4917", "dosage": "0.4mg", "frequency": "As needed (sublingual)", "start_date": d(-14), "end_date": d(76), "refills_remaining": 2, "prescribing_doctor": "D002"},
        {"med_id": "MC009", "patient_id": "P020", "visit_id": "VC008", "drug_name": "Heparin", "rxcui": "5224", "dosage": "5000 units", "frequency": "IV drip", "start_date": d(-14), "end_date": d(-7), "refills_remaining": 0, "prescribing_doctor": "D002"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LC001", "patient_id": "P001", "visit_id": "VC001", "test_name": "Troponin I", "test_date": d(-90), "result_value": "0.02 ng/mL", "reference_range": "<0.04 ng/mL", "status": "Normal"},
        {"lab_id": "LC002", "patient_id": "P001", "visit_id": "VC001", "test_name": "LDL Cholesterol", "test_date": d(-90), "result_value": "165 mg/dL", "reference_range": "<100 mg/dL", "status": "High"},
        {"lab_id": "LC003", "patient_id": "P001", "visit_id": "VC002", "test_name": "LDL Cholesterol", "test_date": d(-30), "result_value": "120 mg/dL", "reference_range": "<100 mg/dL", "status": "Borderline High"},
        {"lab_id": "LC004", "patient_id": "P002", "visit_id": "VC004", "test_name": "BNP", "test_date": d(-60), "result_value": "450 pg/mL", "reference_range": "<100 pg/mL", "status": "High"},
        {"lab_id": "LC005", "patient_id": "P002", "visit_id": "VC004", "test_name": "Echocardiogram EF", "test_date": d(-60), "result_value": "45%", "reference_range": "55-70%", "status": "Below Normal"},
        {"lab_id": "LC006", "patient_id": "P015", "visit_id": "VC007", "test_name": "INR", "test_date": d(-30), "result_value": "2.3", "reference_range": "2.0-3.0", "status": "Therapeutic"},
        {"lab_id": "LC007", "patient_id": "P020", "visit_id": "VC008", "test_name": "Troponin I", "test_date": d(-14), "result_value": "0.08 ng/mL", "reference_range": "<0.04 ng/mL", "status": "Elevated"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


def build_general_medicine():
    visits = pd.DataFrame([
        {"visit_id": "VG001", "patient_id": "P001", "doctor_id": "D005", "visit_date": d(-150), "chief_complaint": "Annual health screening", "diagnosis": "Routine checkup - mild hyperlipidemia", "icd_code": "E78.5", "notes": "Referred to Cardiology for chest tightness.", "follow_up_date": d(-90)},
        {"visit_id": "VG002", "patient_id": "P003", "doctor_id": "D006", "visit_date": d(-200), "chief_complaint": "Knee pain after jogging", "diagnosis": "Knee osteoarthritis", "icd_code": "M17.11", "notes": "Referred to Orthopedics for evaluation.", "follow_up_date": d(-170)},
        {"visit_id": "VG003", "patient_id": "P006", "doctor_id": "D005", "visit_date": d(-60), "chief_complaint": "Increased thirst and urination", "diagnosis": "Type 2 Diabetes Mellitus", "icd_code": "E11.9", "notes": "Started on Metformin 500mg. Diet counseling given.", "follow_up_date": d(0)},
        {"visit_id": "VG004", "patient_id": "P006", "doctor_id": "D005", "visit_date": d(-10), "chief_complaint": "Diabetes follow-up", "diagnosis": "Type 2 Diabetes - controlled", "icd_code": "E11.65", "notes": "HbA1c improving. Continue current treatment.", "follow_up_date": d(80)},
        {"visit_id": "VG005", "patient_id": "P009", "doctor_id": "D012", "visit_date": d(-30), "chief_complaint": "Shortness of breath and wheezing", "diagnosis": "Asthma exacerbation", "icd_code": "J45.41", "notes": "Nebulizer treatment given. Inhaler prescription refilled.", "follow_up_date": d(30)},
        {"visit_id": "VG006", "patient_id": "P012", "doctor_id": "D005", "visit_date": d(-90), "chief_complaint": "Numbness in feet", "diagnosis": "Diabetic neuropathy", "icd_code": "E11.40", "notes": "Referred to Neurology. Gabapentin started.", "follow_up_date": d(-30)},
        {"visit_id": "VG007", "patient_id": "P013", "doctor_id": "D006", "visit_date": d(-20), "chief_complaint": "Pregnancy nausea and fatigue", "diagnosis": "Normal pregnancy - first trimester", "icd_code": "Z34.01", "notes": "Prenatal vitamins prescribed. Routine blood work ordered.", "follow_up_date": d(10)},
        {"visit_id": "VG008", "patient_id": "P018", "doctor_id": "D005", "visit_date": d(-45), "chief_complaint": "Severe allergic reaction to food", "diagnosis": "Anaphylaxis - peanut allergy", "icd_code": "T78.01", "notes": "EpiPen prescribed. Referred to allergy clinic.", "follow_up_date": d(15)},
        {"visit_id": "VG009", "patient_id": "P019", "doctor_id": "D006", "visit_date": d(-100), "chief_complaint": "Tremor in right hand", "diagnosis": "Parkinson's disease - early stage", "icd_code": "G20", "notes": "Referred to Neurology. Initial imaging ordered.", "follow_up_date": d(-60)},
        {"visit_id": "VG010", "patient_id": "P005", "doctor_id": "D005", "visit_date": d(-180), "chief_complaint": "Weight loss and fatigue", "diagnosis": "Suspected malignancy", "icd_code": "R63.4", "notes": "Urgent referral to Oncology. CT scan ordered.", "follow_up_date": d(-160)},
    ])

    medications = pd.DataFrame([
        {"med_id": "MG001", "patient_id": "P006", "visit_id": "VG003", "drug_name": "Metformin", "rxcui": "6809", "dosage": "500mg", "frequency": "Twice daily", "start_date": d(-60), "end_date": d(30), "refills_remaining": 1, "prescribing_doctor": "D005"},
        {"med_id": "MG002", "patient_id": "P009", "visit_id": "VG005", "drug_name": "Salbutamol Inhaler", "rxcui": "196988", "dosage": "100mcg", "frequency": "As needed", "start_date": d(-30), "end_date": d(150), "refills_remaining": 2, "prescribing_doctor": "D012"},
        {"med_id": "MG003", "patient_id": "P012", "visit_id": "VG006", "drug_name": "Metformin", "rxcui": "6809", "dosage": "1000mg", "frequency": "Twice daily", "start_date": d(-180), "end_date": d(3), "refills_remaining": 0, "prescribing_doctor": "D005"},
        {"med_id": "MG004", "patient_id": "P012", "visit_id": "VG006", "drug_name": "Gabapentin", "rxcui": "25480", "dosage": "300mg", "frequency": "Three times daily", "start_date": d(-90), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D005"},
        {"med_id": "MG005", "patient_id": "P013", "visit_id": "VG007", "drug_name": "Folic Acid", "rxcui": "4511", "dosage": "400mcg", "frequency": "Once daily", "start_date": d(-20), "end_date": d(250), "refills_remaining": 5, "prescribing_doctor": "D006"},
        {"med_id": "MG006", "patient_id": "P018", "visit_id": "VG008", "drug_name": "Epinephrine Auto-Injector", "rxcui": "727316", "dosage": "0.3mg", "frequency": "Emergency use", "start_date": d(-45), "end_date": d(320), "refills_remaining": 1, "prescribing_doctor": "D005"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LG001", "patient_id": "P006", "visit_id": "VG003", "test_name": "HbA1c", "test_date": d(-60), "result_value": "8.2%", "reference_range": "<7.0%", "status": "High"},
        {"lab_id": "LG002", "patient_id": "P006", "visit_id": "VG004", "test_name": "HbA1c", "test_date": d(-10), "result_value": "7.1%", "reference_range": "<7.0%", "status": "Borderline High"},
        {"lab_id": "LG003", "patient_id": "P006", "visit_id": "VG004", "test_name": "Fasting Glucose", "test_date": d(-10), "result_value": "135 mg/dL", "reference_range": "70-100 mg/dL", "status": "High"},
        {"lab_id": "LG004", "patient_id": "P012", "visit_id": "VG006", "test_name": "HbA1c", "test_date": d(-90), "result_value": "7.8%", "reference_range": "<7.0%", "status": "High"},
        {"lab_id": "LG005", "patient_id": "P013", "visit_id": "VG007", "test_name": "hCG", "test_date": d(-20), "result_value": "45000 mIU/mL", "reference_range": "Varies by gestational age", "status": "Normal for 8 weeks"},
        {"lab_id": "LG006", "patient_id": "P018", "visit_id": "VG008", "test_name": "IgE Total", "test_date": d(-45), "result_value": "850 IU/mL", "reference_range": "<100 IU/mL", "status": "Very High"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


def build_orthopedics():
    visits = pd.DataFrame([
        {"visit_id": "VO001", "patient_id": "P003", "doctor_id": "D003", "visit_date": d(-170), "chief_complaint": "Severe knee pain, difficulty walking", "diagnosis": "Torn meniscus - left knee", "icd_code": "S83.209A", "notes": "MRI confirms tear. Surgery recommended.", "follow_up_date": d(-140)},
        {"visit_id": "VO002", "patient_id": "P003", "doctor_id": "D003", "visit_date": d(-140), "chief_complaint": "Pre-surgical evaluation", "diagnosis": "Torn meniscus - scheduled for arthroscopy", "icd_code": "S83.209A", "notes": "Surgery scheduled. Pre-op labs ordered.", "follow_up_date": d(-120)},
        {"visit_id": "VO003", "patient_id": "P003", "doctor_id": "D003", "visit_date": d(-100), "chief_complaint": "Post-surgery follow-up", "diagnosis": "Post-arthroscopic meniscus repair", "icd_code": "Z09", "notes": "Healing well. Physical therapy started.", "follow_up_date": d(-30)},
        {"visit_id": "VO004", "patient_id": "P007", "doctor_id": "D003", "visit_date": d(-120), "chief_complaint": "Right hip pain, limited mobility", "diagnosis": "Severe hip osteoarthritis", "icd_code": "M16.11", "notes": "X-ray shows bone-on-bone. Total hip replacement discussed.", "follow_up_date": d(-60)},
        {"visit_id": "VO005", "patient_id": "P010", "doctor_id": "D004", "visit_date": d(-20), "chief_complaint": "Ankle sprain from basketball", "diagnosis": "Grade 2 lateral ankle sprain", "icd_code": "S93.401A", "notes": "RICE protocol. Air cast applied. Follow-up in 2 weeks.", "follow_up_date": d(-6)},
        {"visit_id": "VO006", "patient_id": "P016", "doctor_id": "D014", "visit_date": d(-60), "chief_complaint": "Chronic lower back pain", "diagnosis": "Lumbar disc herniation L4-L5", "icd_code": "M51.16", "notes": "MRI confirms herniation. Conservative treatment first.", "follow_up_date": d(0)},
        {"visit_id": "VO007", "patient_id": "P016", "doctor_id": "D014", "visit_date": d(-10), "chief_complaint": "Back pain not improving", "diagnosis": "Lumbar disc herniation - persistent", "icd_code": "M51.16", "notes": "Epidural steroid injection discussed. Referral to pain clinic.", "follow_up_date": d(20)},
    ])

    medications = pd.DataFrame([
        {"med_id": "MO001", "patient_id": "P003", "visit_id": "VO003", "drug_name": "Celecoxib", "rxcui": "140587", "dosage": "200mg", "frequency": "Once daily", "start_date": d(-100), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D003"},
        {"med_id": "MO002", "patient_id": "P007", "visit_id": "VO004", "drug_name": "Tramadol", "rxcui": "10689", "dosage": "50mg", "frequency": "As needed, max 4x/day", "start_date": d(-120), "end_date": d(-30), "refills_remaining": 0, "prescribing_doctor": "D003"},
        {"med_id": "MO003", "patient_id": "P010", "visit_id": "VO005", "drug_name": "Ibuprofen", "rxcui": "5640", "dosage": "400mg", "frequency": "Three times daily with food", "start_date": d(-20), "end_date": d(10), "refills_remaining": 0, "prescribing_doctor": "D004"},
        {"med_id": "MO004", "patient_id": "P016", "visit_id": "VO006", "drug_name": "Pregabalin", "rxcui": "187832", "dosage": "75mg", "frequency": "Twice daily", "start_date": d(-60), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D014"},
        {"med_id": "MO005", "patient_id": "P016", "visit_id": "VO006", "drug_name": "Diclofenac Gel", "rxcui": "855635", "dosage": "1%", "frequency": "Apply 3 times daily", "start_date": d(-60), "end_date": d(30), "refills_remaining": 1, "prescribing_doctor": "D014"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LO001", "patient_id": "P003", "visit_id": "VO001", "test_name": "MRI Left Knee", "test_date": d(-170), "result_value": "Medial meniscus tear confirmed", "reference_range": "N/A", "status": "Abnormal"},
        {"lab_id": "LO002", "patient_id": "P003", "visit_id": "VO002", "test_name": "CBC Pre-Op", "test_date": d(-142), "result_value": "All values normal", "reference_range": "Standard", "status": "Normal"},
        {"lab_id": "LO003", "patient_id": "P007", "visit_id": "VO004", "test_name": "X-Ray Right Hip", "test_date": d(-120), "result_value": "Severe joint space narrowing, osteophytes", "reference_range": "N/A", "status": "Abnormal"},
        {"lab_id": "LO004", "patient_id": "P016", "visit_id": "VO006", "test_name": "MRI Lumbar Spine", "test_date": d(-61), "result_value": "L4-L5 disc herniation with nerve compression", "reference_range": "N/A", "status": "Abnormal"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


def build_neurology():
    visits = pd.DataFrame([
        {"visit_id": "VN001", "patient_id": "P004", "doctor_id": "D007", "visit_date": d(-120), "chief_complaint": "Recurrent seizures", "diagnosis": "Focal epilepsy", "icd_code": "G40.109", "notes": "EEG shows focal spikes. Started on Levetiracetam.", "follow_up_date": d(-60)},
        {"visit_id": "VN002", "patient_id": "P004", "doctor_id": "D007", "visit_date": d(-30), "chief_complaint": "Seizure frequency follow-up", "diagnosis": "Focal epilepsy - improving", "icd_code": "G40.109", "notes": "Seizure-free for 30 days. Continue medication.", "follow_up_date": d(30)},
        {"visit_id": "VN003", "patient_id": "P008", "doctor_id": "D007", "visit_date": d(-90), "chief_complaint": "Severe migraines 3-4 times weekly", "diagnosis": "Chronic migraine without aura", "icd_code": "G43.709", "notes": "Started on Topiramate for prevention. Sumatriptan for acute.", "follow_up_date": d(-30)},
        {"visit_id": "VN004", "patient_id": "P008", "doctor_id": "D007", "visit_date": d(-15), "chief_complaint": "Migraine follow-up", "diagnosis": "Chronic migraine - frequency reduced", "icd_code": "G43.709", "notes": "Down to 1-2 per week. Continue current regimen.", "follow_up_date": d(45)},
        {"visit_id": "VN005", "patient_id": "P012", "doctor_id": "D008", "visit_date": d(-60), "chief_complaint": "Worsening numbness in feet", "diagnosis": "Diabetic polyneuropathy", "icd_code": "G63", "notes": "Nerve conduction study confirms. Increase Gabapentin.", "follow_up_date": d(30)},
        {"visit_id": "VN006", "patient_id": "P019", "doctor_id": "D007", "visit_date": d(-60), "chief_complaint": "Progressive tremor and stiffness", "diagnosis": "Parkinson's disease", "icd_code": "G20", "notes": "Started on Levodopa/Carbidopa. Occupational therapy referral.", "follow_up_date": d(0)},
    ])

    medications = pd.DataFrame([
        {"med_id": "MN001", "patient_id": "P004", "visit_id": "VN001", "drug_name": "Levetiracetam", "rxcui": "187832", "dosage": "500mg", "frequency": "Twice daily", "start_date": d(-120), "end_date": d(60), "refills_remaining": 2, "prescribing_doctor": "D007"},
        {"med_id": "MN002", "patient_id": "P008", "visit_id": "VN003", "drug_name": "Topiramate", "rxcui": "38404", "dosage": "50mg", "frequency": "Twice daily", "start_date": d(-90), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D007"},
        {"med_id": "MN003", "patient_id": "P008", "visit_id": "VN003", "drug_name": "Sumatriptan", "rxcui": "37418", "dosage": "50mg", "frequency": "As needed for migraine", "start_date": d(-90), "end_date": d(90), "refills_remaining": 3, "prescribing_doctor": "D007"},
        {"med_id": "MN004", "patient_id": "P019", "visit_id": "VN006", "drug_name": "Levodopa/Carbidopa", "rxcui": "393438", "dosage": "100/25mg", "frequency": "Three times daily", "start_date": d(-60), "end_date": d(30), "refills_remaining": 1, "prescribing_doctor": "D007"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LN001", "patient_id": "P004", "visit_id": "VN001", "test_name": "EEG", "test_date": d(-120), "result_value": "Focal epileptiform discharges, left temporal", "reference_range": "Normal background", "status": "Abnormal"},
        {"lab_id": "LN002", "patient_id": "P004", "visit_id": "VN001", "test_name": "MRI Brain", "test_date": d(-118), "result_value": "No structural lesion identified", "reference_range": "N/A", "status": "Normal"},
        {"lab_id": "LN003", "patient_id": "P012", "visit_id": "VN005", "test_name": "Nerve Conduction Study", "test_date": d(-60), "result_value": "Reduced conduction velocity, bilateral lower limbs", "reference_range": ">40 m/s", "status": "Abnormal"},
        {"lab_id": "LN004", "patient_id": "P019", "visit_id": "VN006", "test_name": "DaTscan", "test_date": d(-62), "result_value": "Reduced dopamine transporter uptake", "reference_range": "Symmetric uptake", "status": "Abnormal"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


def build_emergency():
    visits = pd.DataFrame([
        {"visit_id": "VE001", "patient_id": "P002", "doctor_id": "D011", "visit_date": d(-200), "chief_complaint": "Acute chest pain, sweating, SOB", "diagnosis": "ST-elevation myocardial infarction", "icd_code": "I21.09", "notes": "Emergency PCI performed. Transferred to Cardiology ICU.", "follow_up_date": d(-180)},
        {"visit_id": "VE002", "patient_id": "P004", "doctor_id": "D008", "visit_date": d(-150), "chief_complaint": "Seizure at workplace, unconscious", "diagnosis": "Status epilepticus", "icd_code": "G41.0", "notes": "IV Diazepam given. Stabilized. Neurology consulted.", "follow_up_date": d(-120)},
        {"visit_id": "VE003", "patient_id": "P009", "doctor_id": "D012", "visit_date": d(-90), "chief_complaint": "Severe asthma attack, unable to breathe", "diagnosis": "Acute severe asthma", "icd_code": "J46", "notes": "Nebulizer + IV steroids. Admitted for 24h observation.", "follow_up_date": d(-60)},
        {"visit_id": "VE004", "patient_id": "P014", "doctor_id": "D011", "visit_date": d(-7), "chief_complaint": "Motorcycle accident - leg and arm injuries", "diagnosis": "Multiple contusions, right tibial fracture", "icd_code": "S82.101A", "notes": "X-ray confirms fracture. Cast applied. Orthopedics referral.", "follow_up_date": d(7)},
        {"visit_id": "VE005", "patient_id": "P018", "doctor_id": "D011", "visit_date": d(-45), "chief_complaint": "Swollen face and throat after eating peanuts", "diagnosis": "Anaphylactic shock", "icd_code": "T78.2", "notes": "Epinephrine administered. Stabilized. Referred to allergy clinic.", "follow_up_date": d(-30)},
        {"visit_id": "VE006", "patient_id": "P020", "doctor_id": "D002", "visit_date": d(-14), "chief_complaint": "Chest pain radiating to left arm", "diagnosis": "Unstable angina - emergency admission", "icd_code": "I20.0", "notes": "Troponin elevated. Admitted to Cardiology. Heparin started.", "follow_up_date": d(-7)},
    ])

    medications = pd.DataFrame([
        {"med_id": "ME001", "patient_id": "P014", "visit_id": "VE004", "drug_name": "Paracetamol", "rxcui": "161", "dosage": "1000mg", "frequency": "Four times daily", "start_date": d(-7), "end_date": d(7), "refills_remaining": 0, "prescribing_doctor": "D011"},
        {"med_id": "ME002", "patient_id": "P014", "visit_id": "VE004", "drug_name": "Tramadol", "rxcui": "10689", "dosage": "50mg", "frequency": "As needed, max 3x/day", "start_date": d(-7), "end_date": d(7), "refills_remaining": 0, "prescribing_doctor": "D011"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LE001", "patient_id": "P002", "visit_id": "VE001", "test_name": "Troponin I (Emergency)", "test_date": d(-200), "result_value": "5.2 ng/mL", "reference_range": "<0.04 ng/mL", "status": "Critical High"},
        {"lab_id": "LE002", "patient_id": "P002", "visit_id": "VE001", "test_name": "ECG", "test_date": d(-200), "result_value": "ST elevation in leads II, III, aVF", "reference_range": "Normal sinus rhythm", "status": "STEMI"},
        {"lab_id": "LE003", "patient_id": "P014", "visit_id": "VE004", "test_name": "X-Ray Right Leg", "test_date": d(-7), "result_value": "Displaced fracture of proximal tibia", "reference_range": "N/A", "status": "Abnormal"},
        {"lab_id": "LE004", "patient_id": "P020", "visit_id": "VE006", "test_name": "Troponin I (Emergency)", "test_date": d(-14), "result_value": "0.08 ng/mL", "reference_range": "<0.04 ng/mL", "status": "Elevated"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


def build_oncology():
    visits = pd.DataFrame([
        {"visit_id": "VON001", "patient_id": "P005", "doctor_id": "D009", "visit_date": d(-160), "chief_complaint": "Referred for suspected lung malignancy", "diagnosis": "Non-small cell lung carcinoma, Stage IIB", "icd_code": "C34.90", "notes": "Biopsy confirmed. Treatment plan discussed.", "follow_up_date": d(-130)},
        {"visit_id": "VON002", "patient_id": "P005", "doctor_id": "D010", "visit_date": d(-130), "chief_complaint": "Start radiation therapy", "diagnosis": "NSCLC - radiation treatment initiation", "icd_code": "C34.90", "notes": "Radiation therapy cycle 1 started. Weekly monitoring.", "follow_up_date": d(-100)},
        {"visit_id": "VON003", "patient_id": "P005", "doctor_id": "D009", "visit_date": d(-30), "chief_complaint": "Treatment response evaluation", "diagnosis": "NSCLC - partial response to treatment", "icd_code": "C34.90", "notes": "CT shows 40% tumor reduction. Continue treatment.", "follow_up_date": d(30)},
        {"visit_id": "VON004", "patient_id": "P011", "doctor_id": "D009", "visit_date": d(-120), "chief_complaint": "Breast lump found on screening", "diagnosis": "Invasive ductal carcinoma, Stage IA", "icd_code": "C50.919", "notes": "Lumpectomy performed. Adjuvant chemo planned.", "follow_up_date": d(-90)},
        {"visit_id": "VON005", "patient_id": "P011", "doctor_id": "D009", "visit_date": d(-60), "chief_complaint": "Chemotherapy cycle 2", "diagnosis": "Breast cancer - ongoing chemotherapy", "icd_code": "C50.919", "notes": "Tolerating well. Cardiology monitoring due to doxorubicin.", "follow_up_date": d(-30)},
        {"visit_id": "VON006", "patient_id": "P017", "doctor_id": "D009", "visit_date": d(-90), "chief_complaint": "Elevated PSA, referred by GP", "diagnosis": "Prostate adenocarcinoma, Gleason 7", "icd_code": "C61", "notes": "Biopsy confirmed. Hormone therapy started.", "follow_up_date": d(-30)},
        {"visit_id": "VON007", "patient_id": "P017", "doctor_id": "D009", "visit_date": d(-20), "chief_complaint": "Hormone therapy follow-up", "diagnosis": "Prostate cancer - responding to hormone therapy", "icd_code": "C61", "notes": "PSA decreasing. Continue Leuprolide. Next check in 8 weeks.", "follow_up_date": d(36)},
    ])

    medications = pd.DataFrame([
        {"med_id": "MON001", "patient_id": "P005", "visit_id": "VON001", "drug_name": "Carboplatin", "rxcui": "40048", "dosage": "IV per protocol", "frequency": "Every 3 weeks", "start_date": d(-160), "end_date": d(20), "refills_remaining": 0, "prescribing_doctor": "D009"},
        {"med_id": "MON002", "patient_id": "P005", "visit_id": "VON001", "drug_name": "Paclitaxel", "rxcui": "56946", "dosage": "IV per protocol", "frequency": "Every 3 weeks", "start_date": d(-160), "end_date": d(20), "refills_remaining": 0, "prescribing_doctor": "D009"},
        {"med_id": "MON003", "patient_id": "P005", "visit_id": "VON001", "drug_name": "Ondansetron", "rxcui": "26225", "dosage": "8mg", "frequency": "Before chemo + as needed", "start_date": d(-160), "end_date": d(20), "refills_remaining": 0, "prescribing_doctor": "D009"},
        {"med_id": "MON004", "patient_id": "P011", "visit_id": "VON004", "drug_name": "Doxorubicin", "rxcui": "3639", "dosage": "IV per protocol", "frequency": "Every 3 weeks", "start_date": d(-90), "end_date": d(0), "refills_remaining": 0, "prescribing_doctor": "D009"},
        {"med_id": "MON005", "patient_id": "P011", "visit_id": "VON004", "drug_name": "Tamoxifen", "rxcui": "10324", "dosage": "20mg", "frequency": "Once daily", "start_date": d(-90), "end_date": d(1735), "refills_remaining": 10, "prescribing_doctor": "D009"},
        {"med_id": "MON006", "patient_id": "P017", "visit_id": "VON006", "drug_name": "Leuprolide", "rxcui": "6373", "dosage": "7.5mg", "frequency": "Monthly injection", "start_date": d(-90), "end_date": d(90), "refills_remaining": 3, "prescribing_doctor": "D009"},
    ])

    lab_results = pd.DataFrame([
        {"lab_id": "LON001", "patient_id": "P005", "visit_id": "VON001", "test_name": "CT Chest", "test_date": d(-162), "result_value": "3.5cm mass in right upper lobe", "reference_range": "N/A", "status": "Abnormal"},
        {"lab_id": "LON002", "patient_id": "P005", "visit_id": "VON001", "test_name": "Biopsy - Lung", "test_date": d(-160), "result_value": "NSCLC - adenocarcinoma, EGFR positive", "reference_range": "N/A", "status": "Malignant"},
        {"lab_id": "LON003", "patient_id": "P005", "visit_id": "VON003", "test_name": "CT Chest (Follow-up)", "test_date": d(-30), "result_value": "2.1cm mass - partial response", "reference_range": "N/A", "status": "Improved"},
        {"lab_id": "LON004", "patient_id": "P011", "visit_id": "VON004", "test_name": "Mammogram + Ultrasound", "test_date": d(-125), "result_value": "1.2cm mass, left breast, BIRADS 5", "reference_range": "BIRADS 1-2", "status": "Suspicious"},
        {"lab_id": "LON005", "patient_id": "P017", "visit_id": "VON006", "test_name": "PSA", "test_date": d(-92), "result_value": "12.5 ng/mL", "reference_range": "<4.0 ng/mL", "status": "High"},
        {"lab_id": "LON006", "patient_id": "P017", "visit_id": "VON007", "test_name": "PSA", "test_date": d(-20), "result_value": "6.8 ng/mL", "reference_range": "<4.0 ng/mL", "status": "Decreasing"},
    ])

    return {"visits": visits, "medications": medications, "lab_results": lab_results}


# ── Appointments ────────────────────────────────────────────────────────────

APPOINTMENTS = [
    {"appointment_id": "APT0001", "patient_id": "P001", "doctor_id": "D001", "department": "cardiology", "date": d(14), "time": "10:00", "reason": "Angina follow-up", "status": "scheduled"},
    {"appointment_id": "APT0002", "patient_id": "P002", "doctor_id": "D001", "department": "cardiology", "date": d(5), "time": "14:00", "reason": "Cardiac review", "status": "scheduled"},
    {"appointment_id": "APT0003", "patient_id": "P003", "doctor_id": "D003", "department": "orthopedics", "date": d(10), "time": "09:30", "reason": "Post-surgery review", "status": "scheduled"},
    {"appointment_id": "APT0004", "patient_id": "P004", "doctor_id": "D007", "department": "neurology", "date": d(30), "time": "11:00", "reason": "Epilepsy follow-up", "status": "scheduled"},
    {"appointment_id": "APT0005", "patient_id": "P005", "doctor_id": "D009", "department": "oncology", "date": d(30), "time": "09:00", "reason": "Treatment evaluation", "status": "scheduled"},
    {"appointment_id": "APT0006", "patient_id": "P006", "doctor_id": "D005", "department": "general_medicine", "date": d(80), "time": "10:30", "reason": "Diabetes follow-up", "status": "scheduled"},
    {"appointment_id": "APT0007", "patient_id": "P007", "doctor_id": "D013", "department": "cardiology", "date": d(15), "time": "15:00", "reason": "BP follow-up", "status": "scheduled"},
    {"appointment_id": "APT0008", "patient_id": "P008", "doctor_id": "D007", "department": "neurology", "date": d(45), "time": "14:00", "reason": "Migraine follow-up", "status": "scheduled"},
    {"appointment_id": "APT0009", "patient_id": "P011", "doctor_id": "D013", "department": "cardiology", "date": d(30), "time": "11:00", "reason": "Cardiac monitoring (chemo)", "status": "scheduled"},
    {"appointment_id": "APT0010", "patient_id": "P012", "doctor_id": "D008", "department": "neurology", "date": d(30), "time": "10:00", "reason": "Neuropathy follow-up", "status": "scheduled"},
    {"appointment_id": "APT0011", "patient_id": "P013", "doctor_id": "D006", "department": "general_medicine", "date": d(10), "time": "09:00", "reason": "Prenatal checkup", "status": "scheduled"},
    {"appointment_id": "APT0012", "patient_id": "P014", "doctor_id": "D011", "department": "emergency", "date": d(7), "time": "10:00", "reason": "Fracture follow-up", "status": "scheduled"},
    {"appointment_id": "APT0013", "patient_id": "P015", "doctor_id": "D001", "department": "cardiology", "date": d(30), "time": "09:30", "reason": "Warfarin/INR check", "status": "scheduled"},
    {"appointment_id": "APT0014", "patient_id": "P016", "doctor_id": "D014", "department": "orthopedics", "date": d(20), "time": "11:30", "reason": "Back pain follow-up", "status": "scheduled"},
    {"appointment_id": "APT0015", "patient_id": "P017", "doctor_id": "D009", "department": "oncology", "date": d(36), "time": "10:00", "reason": "Hormone therapy review", "status": "scheduled"},
    {"appointment_id": "APT0016", "patient_id": "P019", "doctor_id": "D007", "department": "neurology", "date": d(0), "time": "14:30", "reason": "Parkinson's treatment review", "status": "scheduled"},
    {"appointment_id": "APT0017", "patient_id": "P020", "doctor_id": "D002", "department": "cardiology", "date": d(7), "time": "09:00", "reason": "Angiogram results", "status": "scheduled"},
]


# ── Write everything ────────────────────────────────────────────────────────

def seed():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(PATIENTS).to_excel(DATA_DIR / "patients.xlsx", index=False, engine="openpyxl")
    pd.DataFrame(DOCTORS).to_excel(DATA_DIR / "doctors.xlsx", index=False, engine="openpyxl")
    pd.DataFrame(APPOINTMENTS).to_excel(DATA_DIR / "appointments.xlsx", index=False, engine="openpyxl")

    dept_builders = {
        "cardiology": build_cardiology,
        "general_medicine": build_general_medicine,
        "orthopedics": build_orthopedics,
        "neurology": build_neurology,
        "emergency": build_emergency,
        "oncology": build_oncology,
    }

    for dept, builder in dept_builders.items():
        sheets = builder()
        path = DATA_DIR / f"{dept}.xlsx"
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  ✓ {dept}.xlsx ({sum(len(df) for df in sheets.values())} records)")

    print("\nSeed data generated successfully.")


if __name__ == "__main__":
    seed()
