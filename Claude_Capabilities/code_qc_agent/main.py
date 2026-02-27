"""Entry point for the Code QC Agent.

Usage:
    python main.py

Auto-detects the first file in inputs/source_of_truth/ and inputs/code/,
runs the full QC pipeline, and writes a Word report to outputs/reports/.
"""

import sys
from pathlib import Path


def _find_first_file(directory: str) -> Path | None:
    """Return the first non-.gitkeep file in a directory, or None."""
    d = Path(directory)
    if not d.exists():
        return None
    for f in sorted(d.iterdir()):
        if f.is_file() and f.name not in {".gitkeep", ".DS_Store", "Thumbs.db"}:
            return f
    return None


def main() -> None:
    sot_path = _find_first_file("inputs/source_of_truth")
    code_path = _find_first_file("inputs/code")

    errors: list[str] = []
    if not sot_path:
        errors.append(
            "No source-of-truth file found in inputs/source_of_truth/\n"
            "  → Drop an .xlsx, .docx, or .pdf file there and try again."
        )
    if not code_path:
        errors.append(
            "No code file found in inputs/code/\n"
            "  → Drop a .py, .R, or .sas file there and try again."
        )

    if errors:
        print("ERROR — cannot start pipeline:\n")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)

    print("=" * 60)
    print("  Code QC Agent")
    print("=" * 60)
    print(f"  Source of truth : {sot_path}")
    print(f"  Code file       : {code_path}")
    print("=" * 60)
    print()

    from agents.orchestrator import Orchestrator

    report_path = Orchestrator().run(str(sot_path), str(code_path))

    print()
    print("=" * 60)
    print(f"  Report saved to: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
