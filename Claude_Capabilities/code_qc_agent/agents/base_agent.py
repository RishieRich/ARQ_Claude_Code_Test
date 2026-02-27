"""Base agent — shared Anthropic client, config, and structured-output helper."""

import os
from pathlib import Path
from typing import Type, TypeVar

import anthropic
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Provides a shared Anthropic client and a structured-output call helper."""

    def __init__(self) -> None:
        # Load .env from the project root (parent of agents/)
        project_root = Path(__file__).parent.parent
        load_dotenv(project_root / ".env")

        # Load settings
        config_path = project_root / "config" / "settings.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Always use claude-opus-4-6 regardless of settings.yaml value
        self.model: str = "claude-opus-4-6"
        self.max_tokens: int = config["model"]["max_tokens"]

        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # ------------------------------------------------------------------
    # Content-block helper
    # ------------------------------------------------------------------

    def _make_content_block(self, text: str) -> dict:
        """Wrap text in an API content block, adding prompt-cache hint if large."""
        block: dict = {"type": "text", "text": text}
        if len(text) > 1000:
            block["cache_control"] = {"type": "ephemeral"}
        return block

    # ------------------------------------------------------------------
    # Structured-output call
    # ------------------------------------------------------------------

    def _stream_parse(
        self,
        messages: list[dict],
        system: str,
        output_model: Type[T],
    ) -> T:
        """Call Claude and return a validated Pydantic instance.

        Uses tool_use to guarantee structured JSON output from the model.
        Extended thinking (adaptive) is enabled on every call.
        """
        schema = output_model.model_json_schema()

        response = self.client.messages.create(
            model=self.model,
            system=system,
            messages=messages,
            thinking={"type": "adaptive"},
            tools=[
                {
                    "name": "structured_output",
                    "description": (
                        f"Return the complete {output_model.__name__} object "
                        "with all required fields filled in."
                    ),
                    "input_schema": schema,
                }
            ],
            tool_choice={"type": "tool", "name": "structured_output"},
            max_tokens=self.max_tokens,
        )

        for block in response.content:
            if (
                hasattr(block, "type")
                and block.type == "tool_use"
                and block.name == "structured_output"
            ):
                return output_model.model_validate(block.input)

        raise RuntimeError(
            f"No structured_output tool call found in model response "
            f"(model={self.model}, output_model={output_model.__name__})"
        )
