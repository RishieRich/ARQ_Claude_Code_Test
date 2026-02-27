"""Agent that checks whether the code correctly implements the specification rules."""

import json

from agents.base_agent import BaseAgent
from utils.models import LogicQCResult, ParsedCode, ParsedDoc


class LogicQCAgent(BaseAgent):
    _SYSTEM = (
        "You are an expert QC specialist for statistical and analytical code. "
        "You are given two inputs:\n"
        "1. A structured extraction of a source-of-truth (SOT) specification — domain, "
        "rules, and variable definitions.\n"
        "2. A structured extraction of the code under review — what it does, its sections, "
        "variables, transformations, and filters.\n\n"
        "Your task: compare the code against every rule in the specification and produce "
        "a QC finding for each rule.\n\n"
        "For each rule:\n"
        "- PASS   — the code clearly and correctly implements the rule.\n"
        "- FAIL   — the code is missing, contradicts, or clearly mis-implements the rule.\n"
        "- WARNING — the code partially implements the rule, or the implementation is "
        "ambiguous / cannot be verified from the information available.\n\n"
        "Also add findings for any code behaviours that have no corresponding specification "
        "rule (undocumented logic).\n\n"
        "Each finding must include:\n"
        "- title: short, specific label for the rule or issue.\n"
        "- status: PASS / FAIL / WARNING.\n"
        "- detail: what was found in the code (or not found).\n"
        "- recommendation: actionable step to resolve (or 'None required' for PASS).\n"
        "- priority: High / Medium / Low based on potential business impact."
    )

    def check(self, parsed_doc: ParsedDoc, parsed_code: ParsedCode) -> LogicQCResult:
        """Run a logic QC comparison and return structured findings."""
        prompt = (
            "Please perform a Logic QC check using the inputs below.\n\n"
            "=== SPECIFICATION (Source of Truth) ===\n"
            f"{json.dumps(parsed_doc.model_dump(), indent=2)}\n\n"
            "=== CODE ANALYSIS ===\n"
            f"{json.dumps(parsed_code.model_dump(), indent=2)}\n\n"
            "Check every rule in the specification against what the code implements. "
            "Generate one finding per rule, and additional findings for any undocumented "
            "code logic you observe."
        )

        content_block = self._make_content_block(prompt)
        messages = [{"role": "user", "content": [content_block]}]
        return self._stream_parse(messages, self._SYSTEM, LogicQCResult)
