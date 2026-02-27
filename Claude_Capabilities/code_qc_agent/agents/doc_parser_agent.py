"""Agent that parses a source-of-truth document into structured rules and variables."""

from agents.base_agent import BaseAgent
from utils.models import ParsedDoc


class DocParserAgent(BaseAgent):
    _SYSTEM = (
        "You are an expert domain specification analyst. "
        "Your task is to carefully read source-of-truth (SOT) documentation — "
        "which may be a regulatory spec, a business rules document, or a statistical "
        "analysis plan — and extract every rule, variable definition, condition, and "
        "source reference into a clean structured format.\n\n"
        "Guidelines:\n"
        "- Identify the overall domain (e.g. 'SDTM derivation', 'claims adjudication', "
        "'financial reporting').\n"
        "- For each distinct rule or requirement, capture: title, full description, "
        "relevant variable names, any explicit conditions or criteria, and a source "
        "reference (page, section, row number, etc.) if available.\n"
        "- For each variable defined in the document, capture: name, definition, and "
        "any expected transformation or derivation logic.\n"
        "- Be exhaustive — do not skip implicit rules or edge-case conditions."
    )

    def parse(self, sot_text: str) -> ParsedDoc:
        """Parse the full SOT text and return a structured ParsedDoc."""
        content_block = self._make_content_block(sot_text)
        messages = [
            {
                "role": "user",
                "content": [
                    content_block,
                    {
                        "type": "text",
                        "text": (
                            "Please analyse the document above and extract all rules, "
                            "variable definitions, and conditions into the structured format."
                        ),
                    },
                ],
            }
        ]
        return self._stream_parse(messages, self._SYSTEM, ParsedDoc)
