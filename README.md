# CareBridge — Intelligent Hospital Reception Assistant

Agentic chatbot that assists hospital receptionists with patient management, appointment scheduling, medication tracking, and clinical decision support.

## Architecture

```
Orchestrator (Aggregator Agent)
├── Department Agents (×6)     — scoped DB access per department
│   ├── cardiology
│   ├── orthopedics
│   ├── general_medicine
│   ├── neurology
│   ├── emergency
│   └── oncology
├── Drug Interaction Agent     — RxNorm + OpenFDA APIs
├── ICD-10 Classification Agent — WHO ICD API + local fallback
└── Triage Agent               — urgency classification & routing
```

Each agent uses OpenAI function calling. The orchestrator receives user queries and dispatches to the appropriate sub-agent(s), then aggregates results.

## Features

| Feature | Description |
|---------|-------------|
| Patient Search | FIN (last 4 digits), name, phone, email, DOB — any combination |
| Cross-Dept Records | Visit history, medications, lab results across 6 departments |
| Appointment Mgmt | Check doctor availability, book/view appointments |
| Medication Alerts | Flags meds expiring before next appointment, low refills |
| Drug Interactions | RxNorm drug-drug interaction checks + OpenFDA label info |
| ICD-10 Coding | WHO ICD API search with local fallback for common codes |
| Triage & Routing | Symptom-based urgency classification → department routing |
| MC Generation | Medical certificate generation (pending doctor approval) |

## Project Structure

```
├── app.py                    # Streamlit entry point
├── config/
│   └── settings.py           # Environment config
├── src/
│   ├── agents/
│   │   ├── base.py           # Base agent with function-calling loop
│   │   ├── orchestrator.py   # Top-level aggregator
│   │   ├── department_agent.py
│   │   ├── drug_agent.py
│   │   ├── icd_agent.py
│   │   └── triage_agent.py
│   ├── tools/
│   │   ├── patient_search.py
│   │   ├── appointment.py
│   │   ├── medical_records.py
│   │   ├── drug_api.py
│   │   ├── icd_api.py
│   │   └── mc_generator.py
│   ├── db/
│   │   └── excel_store.py    # Excel-backed data layer
│   └── llm/
│       └── client.py         # OpenAI API wrapper
├── data/                     # Generated Excel data (gitignored)
│   ├── patients.xlsx
│   ├── doctors.xlsx
│   ├── appointments.xlsx
│   └── <department>.xlsx
├── scripts/
│   └── seed_data.py          # Generates sample Excel datasets
└── docs/
    ├── HACKATHON_PROBLEM_STATEMENT.md
    └── api_openapi_spec.json
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env — add your OpenAI API key

# 3. Generate sample data
python scripts/seed_data.py

# 4. Run the app
streamlit run app.py
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_MODEL` | No | Model to use (default: `gpt-4o-mini`) |
| `ICD_CLIENT_ID` | No | WHO ICD API client ID (for live ICD lookups) |
| `ICD_CLIENT_SECRET` | No | WHO ICD API client secret |

## Example Queries

- "Search for patient with FIN ending 2345"
- "Show me Tan Wei Ming's visit history across all departments"
- "What medications is patient P001 currently on? Are any expiring soon?"
- "Check if Warfarin and Aspirin have any interactions"
- "Patient is complaining of chest pain and has a history of heart problems — triage"
- "What's the ICD-10 code for type 2 diabetes with neuropathy?"
- "Book an appointment with Dr. Tan Beng Choo in cardiology for next Monday"
- "Generate an MC for patient P014 — Dr. Sarah Tan approved 3 days for tibial fracture"

## Data Model

The other team maintains the actual database. This app uses Excel files as a stand-in:

- **patients.xlsx**: 20 patients with Singapore-context demographics (FIN, NRIC, phone, allergies)
- **doctors.xlsx**: 15 doctors, some working across multiple departments
- **appointments.xlsx**: Scheduled appointments
- **Per-department Excel**: Sheets for `visits`, `medications`, `lab_results`

Sample data includes cross-department patients, medication expiry scenarios, and drug interaction cases for demo purposes.
