# Code QC Agent Flow Explanation

This file explains how the `code_qc_agent` runs, in simple and correct order.

## 1. Start point: `main.py`

When you run:

```bash
python main.py
```

`main.py` does this:
1. Looks inside `inputs/source_of_truth/` and picks the first valid file (ignores `.gitkeep`).
2. Looks inside `inputs/code/` and picks the first valid file.
3. If either is missing, it stops with an error message.
4. If both exist, it calls `Orchestrator().run(sot_path, code_path)`.

## 2. Main pipeline: `agents/orchestrator.py`

The orchestrator runs **7 sequential steps**:

1. Read source-of-truth file (Excel/Word/PDF) using `utils.file_reader.read_sot_file`.
2. Read code file (Python/R/SAS) using `utils.file_reader.read_code_file`.
3. Parse source-of-truth text with `DocParserAgent` into structured `ParsedDoc`.
4. Parse code with `CodeParserAgent` into structured `ParsedCode`.
5. Run logic comparison with `LogicQCAgent` -> `LogicQCResult`.
6. Run structure/quality review with `StructureQCAgent` -> `StructureQCResult`.
7. Generate final `.docx` report with `ReportAgent`.

Important: these steps are currently done one after another (not parallel).

## 3. What each agent does

## `BaseAgent` (shared setup)
- Loads `.env` from project root.
- Reads `config/settings.yaml` for `max_tokens`.
- Creates Anthropic client with `ANTHROPIC_API_KEY`.
- Uses structured tool output (`structured_output`) so LLM responses map into Pydantic models.
- Model is hard-set to `claude-opus-4-6`.

## `DocParserAgent`
- Input: full source-of-truth text.
- Output: `ParsedDoc` with:
  - `domain`
  - `rules[]`
  - `variables[]`

## `CodeParserAgent`
- Input: raw code + detected language.
- Output: `ParsedCode` with:
  - summary
  - sections
  - variables
  - transformations
  - filters
  - hardcoded values

## `LogicQCAgent`
- Input: parsed doc + parsed code.
- Compares spec rules vs implemented code logic.
- Output: `LogicQCResult` containing `findings[]` with PASS/FAIL/WARNING and recommendations.

## `StructureQCAgent`
- Input: parsed code + raw code.
- Checks maintainability and quality (naming, hardcoding, organization, docs, duplication, etc.).
- Output: `StructureQCResult` containing `findings[]`.

## `ReportAgent`
- No LLM call here.
- Builds a timestamped Word report using `utils/doc_writer.py`.
- Saves to `outputs/reports/qc_report_YYYYMMDD_HHMMSS.docx`.

## 4. File reading behavior (`utils/file_reader.py`)

- Source-of-truth supports:
  - `.xlsx` via `openpyxl` (all sheets, row text)
  - `.docx` via `python-docx` (paragraphs + tables)
  - `.pdf` via `pdfplumber` (page text)
- Code supports:
  - `.py` -> `python`
  - `.r` -> `r`
  - `.sas` -> `sas`

If format is unsupported, it raises `ValueError`.

## 5. Data contract (`utils/models.py`)

The pipeline uses Pydantic models between steps, so each stage gets structured data, not free text.

Both QC result models auto-calculate:
- `pass_count`
- `fail_count`
- `warning_count`

from the findings list using model validators.

## 6. Final output report (`utils/doc_writer.py`)

The generated Word report contains:
1. Title + metadata
2. Executive Summary table (Logic QC + Structure QC + Total)
3. Logic QC Findings table
4. Structure QC Findings table

Status cells are color-coded:
- PASS = green
- FAIL = red
- WARNING = orange

## 7. Quick mental model

Use this simple flow:

Input files -> Text/code read -> Parsed spec + parsed code -> Two QC checks -> Word report.

