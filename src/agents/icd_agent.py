"""
ICD-10/11 classification sub-agent — wraps WHO ICD API with local fallback.
"""

from src.agents.base import BaseAgent
from src.tools import icd_api


class ICDAgent(BaseAgent):
    """Agent for ICD code lookups and classification."""

    name = "icd_agent"

    def __init__(self, model=None):
        super().__init__(model=model)

        self.system_prompt = """You are an ICD-10/ICD-11 medical coding assistant for MediGuard Hospital.

Your capabilities:
- Search for ICD codes given a diagnosis description
- Retrieve details for specific ICD codes
- Help verify that the correct ICD code is assigned to a diagnosis

When presenting results:
1. Show the most relevant code first
2. Include the full code description
3. If multiple codes could apply, list alternatives with brief explanations
4. Note the ICD version (ICD-10 vs ICD-11)

This information helps ensure accurate medical coding for billing and records."""

        self._register_tools()

    def _register_tools(self):
        self.tool_schemas.append(icd_api.SCHEMA_SEARCH_ICD)
        self.tool_handlers["search_icd_code"] = icd_api.search_icd_code

        self.tool_schemas.append(icd_api.SCHEMA_GET_ICD)
        self.tool_handlers["get_icd_details"] = icd_api.get_icd_details
