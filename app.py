"""
MediGuard AI — Streamlit Application

Hospital receptionist chatbot powered by an agentic multi-agent architecture.
"""

import streamlit as st
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.settings import OPENAI_API_KEY, DEPARTMENTS
from src.db.excel_store import ExcelStore
from src.agents.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")

# ── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MediGuard AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ──────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state.store = ExcelStore()

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator(store=st.session_state.store)

if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# ── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://img.icons8.com/color/96/hospital-3.png", width=60)
    st.title("MediGuard AI")
    st.caption("Intelligent Hospital Reception Assistant")

    st.divider()

    # API key check
    if not OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not configured. Create a `.env` file from `.env.example`.")
    else:
        st.success("✅ API connected")

    st.divider()

    # Quick actions
    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Search Patient", use_container_width=True):
            st.session_state.quick_action = "search"
    with col2:
        if st.button("📅 Book Appt", use_container_width=True):
            st.session_state.quick_action = "book"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("💊 Drug Check", use_container_width=True):
            st.session_state.quick_action = "drug"
    with col4:
        if st.button("🚨 Triage", use_container_width=True):
            st.session_state.quick_action = "triage"

    col5, col6 = st.columns(2)
    with col5:
        if st.button("🏷️ ICD Lookup", use_container_width=True):
            st.session_state.quick_action = "icd"
    with col6:
        if st.button("📄 Generate MC", use_container_width=True):
            st.session_state.quick_action = "mc"

    st.divider()

    # Current patient context
    st.subheader("Current Patient")
    if st.session_state.current_patient:
        p = st.session_state.current_patient
        st.markdown(f"**{p.get('name', 'N/A')}**")
        st.markdown(f"FIN: `{p.get('fin_number', 'N/A')}`")
        st.markdown(f"DOB: {p.get('dob', 'N/A')}")
        st.markdown(f"Allergies: {p.get('allergies', 'None')}")
        if st.button("Clear Patient", use_container_width=True):
            st.session_state.current_patient = None
            st.rerun()
    else:
        st.info("No patient selected. Search for a patient to load their context.")

    st.divider()

    # Department filter
    st.subheader("Departments")
    for dept in DEPARTMENTS:
        st.markdown(f"• {dept.replace('_', ' ').title()}")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_patient = None
        st.rerun()


# ── Pre-fill from quick actions ─────────────────────────────────────────────

QUICK_ACTION_PROMPTS = {
    "search": "I need to find a patient. Can you help me search?",
    "book": "I need to book an appointment for a patient.",
    "drug": "I need to check for drug interactions between medications.",
    "triage": "A patient just walked in with symptoms. Help me triage.",
    "icd": "I need to look up an ICD-10 code for a diagnosis.",
    "mc": "I need to generate a medical certificate for a patient.",
}

# ── Main chat area ──────────────────────────────────────────────────────────

st.title("🏥 MediGuard AI")
st.caption("Your intelligent hospital reception assistant — search patients, manage appointments, check medications, and more.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle quick action pre-fills
quick_action = st.session_state.pop("quick_action", None)
prefill = QUICK_ACTION_PROMPTS.get(quick_action, "")

# Chat input
if prompt := st.chat_input("Type your message...", key="chat_input"):
    user_input = prompt
elif prefill:
    user_input = prefill
else:
    user_input = None

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build context from current patient
                context = None
                if st.session_state.current_patient:
                    p = st.session_state.current_patient
                    context = f"Current patient in context: {p.get('name')} (ID: {p.get('patient_id')}, FIN: {p.get('fin_number')})"

                # Build conversation history for the orchestrator
                # Send only the last few messages for context
                history = st.session_state.messages[-10:]
                history_text = "\n".join(
                    f"{'Receptionist' if m['role'] == 'user' else 'MediGuard'}: {m['content']}"
                    for m in history[:-1]  # exclude current message
                )
                if history_text:
                    full_context = f"Conversation history:\n{history_text}"
                    if context:
                        full_context = f"{context}\n\n{full_context}"
                else:
                    full_context = context

                response = st.session_state.orchestrator.run(
                    user_input,
                    context=full_context,
                )

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Try to detect if a patient was identified in the response
                # (simple heuristic — look for patient ID patterns)
                _try_extract_patient(response)

            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


def _try_extract_patient(response):
    """Try to auto-set current patient from agent response."""
    import re
    match = re.search(r'\b(P\d{3})\b', response)
    if match and not st.session_state.current_patient:
        patient_id = match.group(1)
        patient = st.session_state.store.get_patient(patient_id)
        if patient:
            st.session_state.current_patient = patient
