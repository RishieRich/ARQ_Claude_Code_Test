"""Agent that assesses code quality, structure, and maintainability."""

import json

from agents.base_agent import BaseAgent
from utils.models import ParsedCode, StructureQCResult


class StructureQCAgent(BaseAgent):
    _SYSTEM = (
        "You are an expert code quality reviewer specialising in analytical and "
        "statistical programs ({language}).\n\n"
        "You are given a structured summary of the code and the raw code itself. "
        "Assess the following structural quality dimensions and produce a QC finding "
        "for each:\n\n"
        "1. Naming conventions — are variables, datasets, and functions named clearly "
        "and consistently?\n"
        "2. Hardcoded values — are literal magic numbers, dates, or strings embedded "
        "that should be parameters or constants?\n"
        "3. Code organisation — is the code logically structured with clear sections?\n"
        "4. Documentation — are there adequate comments explaining non-obvious logic?\n"
        "5. Error handling — does the code handle missing data, edge cases, or invalid "
        "inputs gracefully?\n"
        "6. Modularity — is the code appropriately broken into reusable functions or "
        "macros, or is it a single monolithic block?\n"
        "7. Duplication — are there repeated code blocks that should be abstracted?\n"
        "8. Any other structural issues you identify.\n\n"
        "For each finding:\n"
        "- PASS   — meets acceptable quality standards.\n"
        "- FAIL   — clear violation of best practices that could cause errors or "
        "maintenance burden.\n"
        "- WARNING — concerns that should be addressed but are not immediately harmful.\n\n"
        "Include: title, status, specific detail, actionable recommendation, priority."
    )

    def check(self, parsed_code: ParsedCode, raw_code: str) -> StructureQCResult:
        """Run a structure QC assessment and return structured findings."""
        prompt = (
            "Please perform a Structure QC review of the code below.\n\n"
            "=== CODE ANALYSIS SUMMARY ===\n"
            f"{json.dumps(parsed_code.model_dump(), indent=2)}\n\n"
            "=== RAW CODE ===\n"
            f"{raw_code}\n\n"
            "Assess all structural quality dimensions described in your instructions "
            "and return a finding for each."
        )

        content_block = self._make_content_block(prompt)
        messages = [{"role": "user", "content": [content_block]}]

        system = self._SYSTEM.replace("{language}", parsed_code.language.upper())
        return self._stream_parse(messages, system, StructureQCResult)
