"""Report agent — deterministic Word document generation (no LLM call)."""

from datetime import datetime
from pathlib import Path

from utils.doc_writer import write_report
from utils.models import LogicQCResult, StructureQCResult


class ReportAgent:
    """Generates the QC Word report from structured results."""

    def generate(
        self,
        sot_path: str,
        code_path: str,
        logic_result: LogicQCResult,
        structure_result: StructureQCResult,
        output_dir: str,
    ) -> str:
        """Write the report and return the absolute path to the saved .docx file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir) / f"qc_report_{timestamp}.docx"

        write_report(
            sot_path=sot_path,
            code_path=code_path,
            logic_result=logic_result,
            structure_result=structure_result,
            output_path=str(output_path),
        )

        return str(output_path.resolve())
