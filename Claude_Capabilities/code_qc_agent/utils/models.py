"""Shared Pydantic data models for the Code QC Agent pipeline."""

from typing import Literal
from pydantic import BaseModel, model_validator


class Rule(BaseModel):
    title: str
    description: str
    variables: list[str] = []
    conditions: list[str] = []
    source_ref: str = ""


class VarDef(BaseModel):
    name: str
    definition: str
    expected_transform: str = ""


class ParsedDoc(BaseModel):
    domain: str
    rules: list[Rule]
    variables: list[VarDef]


class Section(BaseModel):
    name: str
    description: str
    code_snippet: str
    line_range: str = ""


class ParsedCode(BaseModel):
    language: str  # "python" | "r" | "sas"
    summary: str
    sections: list[Section]
    variables: list[str]
    transformations: list[str]
    filters: list[str]
    hardcoded_values: list[str]


class QCFinding(BaseModel):
    title: str
    status: Literal["PASS", "FAIL", "WARNING"]
    detail: str
    recommendation: str
    priority: Literal["High", "Medium", "Low"]


class LogicQCResult(BaseModel):
    findings: list[QCFinding]
    pass_count: int = 0
    fail_count: int = 0
    warning_count: int = 0

    @model_validator(mode="after")
    def compute_counts(self) -> "LogicQCResult":
        self.pass_count = sum(1 for f in self.findings if f.status == "PASS")
        self.fail_count = sum(1 for f in self.findings if f.status == "FAIL")
        self.warning_count = sum(1 for f in self.findings if f.status == "WARNING")
        return self


class StructureQCResult(BaseModel):
    findings: list[QCFinding]
    pass_count: int = 0
    fail_count: int = 0
    warning_count: int = 0

    @model_validator(mode="after")
    def compute_counts(self) -> "StructureQCResult":
        self.pass_count = sum(1 for f in self.findings if f.status == "PASS")
        self.fail_count = sum(1 for f in self.findings if f.status == "FAIL")
        self.warning_count = sum(1 for f in self.findings if f.status == "WARNING")
        return self
