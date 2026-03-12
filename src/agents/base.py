"""
Base agent with function-calling loop.

Every agent has a system prompt, a set of tools, and runs an iterative
tool-calling loop against the LLM until a final text response is produced.
"""

import json
import logging
from src.llm.client import llm_client
from config.settings import MAX_AGENT_ITERATIONS

logger = logging.getLogger(__name__)


class BaseAgent:
    """
    An LLM agent that can use tools via OpenAI-compatible function calling.

    Subclasses populate `self.tool_schemas` (list of JSON tool defs) and
    `self.tool_handlers` (dict mapping function name → callable).
    """

    name: str = "base"
    system_prompt: str = "You are a helpful assistant."

    def __init__(self, model=None):
        self.model = model
        self.tool_schemas = []       # populated by subclass
        self.tool_handlers = {}      # name → callable

    def run(self, user_message, context=None):
        """
        Execute the agent loop:
        1. Send messages + tools to LLM
        2. If LLM returns tool_calls, execute them and feed results back
        3. Repeat until LLM returns a text response (or max iterations)
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        if context:
            messages.append({"role": "system", "content": f"Additional context:\n{context}"})
        messages.append({"role": "user", "content": user_message})

        for iteration in range(MAX_AGENT_ITERATIONS):
            logger.debug(f"[{self.name}] iteration {iteration + 1}")

            response = llm_client.chat(
                messages,
                model=self.model,
                tools=self.tool_schemas if self.tool_schemas else None,
            )

            choice = response["choices"][0]
            msg = choice["message"]

            # No tool calls → final answer
            if not msg.get("tool_calls"):
                return msg.get("content", "")

            # Append assistant message with tool calls
            messages.append(msg)

            # Execute each tool call
            for tc in msg["tool_calls"]:
                fn_name = tc["function"]["name"]
                try:
                    fn_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    fn_args = {}

                handler = self.tool_handlers.get(fn_name)
                if handler:
                    try:
                        result = handler(**fn_args)
                    except Exception as e:
                        logger.error(f"[{self.name}] tool {fn_name} error: {e}")
                        result = {"error": str(e)}
                else:
                    result = {"error": f"Unknown tool: {fn_name}"}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": json.dumps(result, default=str),
                })

        return "I've reached the maximum number of reasoning steps. Please try a more specific query."
