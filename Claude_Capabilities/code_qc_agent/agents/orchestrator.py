"""Orchestrator — runs the full QC pipeline sequentially."""

from utils import file_reader
from agents.doc_parser_agent import DocParserAgent
from agents.code_parser_agent import CodeParserAgent
from agents.logic_qc_agent import LogicQCAgent
from agents.structure_qc_agent import StructureQCAgent
from agents.report_agent import ReportAgent


class Orchestrator:
    """Drives each pipeline step in order and prints progress."""

    def run(self, sot_path: str, code_path: str) -> str:
        """Execute the full pipeline and return the path to the generated report."""

        # Step 1 — Read files
        print("[1/7] Reading source-of-truth file...")
        sot_text = file_reader.read_sot_file(sot_path)
        print(f"      {len(sot_text):,} characters read.")

        print("[2/7] Reading code file...")
        raw_code, language = file_reader.read_code_file(code_path)
        print(f"      Language: {language} | {len(raw_code):,} characters read.")

        # Step 2 — Parse documents
        print("[3/7] Parsing specification document with DocParserAgent...")
        parsed_doc = DocParserAgent().parse(sot_text)
        print(
            f"      Domain: {parsed_doc.domain!r} | "
            f"{len(parsed_doc.rules)} rule(s) | "
            f"{len(parsed_doc.variables)} variable(s) extracted."
        )

        print("[4/7] Parsing code structure with CodeParserAgent...")
        parsed_code = CodeParserAgent().parse(raw_code, language)
        print(
            f"      {len(parsed_code.sections)} section(s) | "
            f"{len(parsed_code.variables)} variable(s) | "
            f"{len(parsed_code.hardcoded_values)} hardcoded value(s) found."
        )

        # Step 3 — QC checks
        print("[5/7] Running Logic QC...")
        logic_result = LogicQCAgent().check(parsed_doc, parsed_code)
        print(
            f"      PASS: {logic_result.pass_count} | "
            f"FAIL: {logic_result.fail_count} | "
            f"WARNING: {logic_result.warning_count}"
        )

        print("[6/7] Running Structure QC...")
        structure_result = StructureQCAgent().check(parsed_code, raw_code)
        print(
            f"      PASS: {structure_result.pass_count} | "
            f"FAIL: {structure_result.fail_count} | "
            f"WARNING: {structure_result.warning_count}"
        )

        # Step 4 — Generate report
        print("[7/7] Generating Word report...")
        report_path = ReportAgent().generate(
            sot_path=sot_path,
            code_path=code_path,
            logic_result=logic_result,
            structure_result=structure_result,
            output_dir="outputs/reports",
        )

        return report_path
