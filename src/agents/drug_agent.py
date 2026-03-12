"""
Drug interaction sub-agent — wraps RxNorm + OpenFDA APIs.
"""

from src.agents.base import BaseAgent
from src.tools import drug_api


class DrugAgent(BaseAgent):
    """Agent for drug lookups, interaction checks, and label information."""

    name = "drug_agent"

    def __init__(self, model=None):
        super().__init__(model=model)

        self.system_prompt = """You are a pharmaceutical reference assistant for MediGuard Hospital.

Your capabilities:
- Look up drug identifiers (RxCUI) from drug names
- Check drug-drug interactions between multiple medications
- Retrieve detailed drug label information (warnings, contraindications, interactions)

When reporting interactions:
1. Clearly state the severity (major, moderate, minor)
2. Explain the clinical significance in plain language
3. Suggest what the receptionist should flag for the doctor

Always note that drug interaction information is for reference only and clinical decisions
should be made by the attending physician."""

        self._register_tools()

    def _register_tools(self):
        self.tool_schemas.append(drug_api.SCHEMA_DRUG_LOOKUP)
        self.tool_handlers["lookup_drug_rxcui"] = drug_api.lookup_drug_rxcui

        self.tool_schemas.append(drug_api.SCHEMA_DRUG_INTERACTION)
        self.tool_handlers["check_drug_interactions"] = drug_api.check_drug_interactions

        self.tool_schemas.append(drug_api.SCHEMA_DRUG_INFO)
        self.tool_handlers["get_drug_info"] = drug_api.get_drug_info
