"""Agent that parses source code into a structured summary."""

from agents.base_agent import BaseAgent
from utils.models import ParsedCode


class CodeParserAgent(BaseAgent):

    def parse(self, code: str, language: str) -> ParsedCode:
        """Analyse code and return a structured ParsedCode."""
        system = (
            f"You are an expert code analyst specialising in {language.upper()} programs "
            "used for statistical analysis, data processing, or reporting.\n\n"
            "Your task is to read the provided code and extract:\n"
            "- A plain-language summary of what the code does overall.\n"
            "- A list of logical sections (e.g. data import, filtering, derivation, output), "
            "each with a name, description, representative code snippet, and approximate "
            "line range.\n"
            "- All variable names referenced or created.\n"
            "- All data transformations performed (merges, derives, recodes, formats).\n"
            "- All filter or subsetting operations applied.\n"
            "- All hardcoded literal values (magic numbers, inline strings, date literals) "
            "that should probably be parameters.\n\n"
            "Be specific and complete — this output will be used for automated QC."
        )

        content_block = self._make_content_block(code)
        messages = [
            {
                "role": "user",
                "content": [
                    content_block,
                    {
                        "type": "text",
                        "text": (
                            "Please analyse the code above and return the complete "
                            "structured breakdown."
                        ),
                    },
                ],
            }
        ]
        return self._stream_parse(messages, system, ParsedCode)
