# Code QC Agent — Multi-Agent Quality Check System

## What This Does

A multi-agent system that validates analytical code (Python, R, SAS) against a domain-specific
source of truth document (Excel, Word, PDF). It produces a clean, non-technical Word report
summarizing what was checked, what passed, and what needs attention.

Designed for users who are not code reviewers — the output is a structured report they can read
and act on without needing to understand the code itself.

---

## Inputs

| Input | Supported Formats | Description |
|-------|------------------|-------------|
| Source of Truth | `.xlsx` (multi-sheet), `.docx`, `.pdf` | Domain spec, business rules, variable definitions, logic guidelines |
| Code to QC | `.py`, `.R`, `.sas` | Analytical or statistical code to validate |

---

## What Gets Checked

### 1. Logic QC
- Does the code follow the business rules and formulas defined in the source of truth?
- Are variable transformations consistent with documented specs?
- Are filters, conditions, and groupings aligned with what's described?

### 2. Structure QC
- Is the code organized in a readable, maintainable way?
- Are variable and function names meaningful?
- Are there undocumented assumptions or hardcoded magic values?
- Is the flow logical (data load → clean → transform → output)?

---

## Output

A formatted **Word document** (`.docx`) containing:
- Executive summary (pass/fail/warning counts)
- Logic QC findings per rule/section
- Structure QC observations
- Recommendation table (what to fix, priority level)

---

## Agent Architecture

```
User Input
    │
    ▼
┌─────────────────────────┐
│   Orchestrator Agent    │  ← Coordinates the full pipeline
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  Doc Parser  │  │ Code Parser  │  ← Run in parallel
│    Agent     │  │   Agent      │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬─────────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  Logic QC    │  │ Structure QC │  ← Both run after parsing
│    Agent     │  │    Agent     │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬─────────┘
                ▼
     ┌─────────────────────┐
     │  Report Generator   │  ← Compiles findings into Word doc
     │      Agent          │
     └─────────────────────┘
```

---

## Agents — Roles & Responsibilities

| Agent | Role |
|-------|------|
| **Orchestrator** | Accepts inputs, routes files to correct parsers, sequences downstream agents, collects results |
| **Doc Parser** | Reads Excel (all sheets), Word, or PDF and extracts structured rules, variable definitions, and specs |
| **Code Parser** | Reads Python/R/SAS and extracts logic blocks, variable names, transformations, filters, and flow |
| **Logic QC** | Compares parsed code logic against parsed source-of-truth rules; flags mismatches |
| **Structure QC** | Assesses code organization, naming, hardcoding, flow clarity; gives structural recommendations |
| **Report Generator** | Takes all findings and assembles a clean, readable Word report for non-technical users |

---

## Folder Structure

```
code_qc_agent/
├── README.md
├── main.py                    # Entry point — run this
├── requirements.txt
├── .env.example
│
├── config/
│   └── settings.yaml          # Model, paths, report options
│
├── agents/                    # One file per agent (to be built)
│   └── __init__.py
│
├── utils/                     # Shared helpers (file I/O, formatters)
│   └── __init__.py
│
├── inputs/
│   ├── source_of_truth/       # Drop your Excel/Word/PDF here
│   └── code/                  # Drop your Python/R/SAS here
│
└── outputs/
    └── reports/               # Generated Word reports land here
```

---

## Tech Stack (Planned)

| Purpose | Library |
|---------|---------|
| LLM backbone | Anthropic Claude (claude-sonnet-4-6) |
| Agent orchestration | Anthropic Agent SDK |
| Excel parsing | `openpyxl` |
| Word parsing & output | `python-docx` |
| PDF parsing | `pdfplumber` |
| SAS/R/Python parsing | AST + regex based |

---

## Status

- [x] README and project structure defined
- [ ] Doc Parser Agent
- [ ] Code Parser Agent
- [ ] Logic QC Agent
- [ ] Structure QC Agent
- [ ] Report Generator Agent
- [ ] Orchestrator Agent
- [ ] End-to-end test with sample inputs
