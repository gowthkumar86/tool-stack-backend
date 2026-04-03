from typing import Literal

from pydantic import BaseModel, Field


NormalizationMode = Literal["lower", "upper", "title"]


class GLiNERRequest(BaseModel):
    """Backward-compatible request model."""

    text: str = Field(..., min_length=1)
    labels: list[str] = Field(..., min_items=1)


class Entity(BaseModel):
    text: str
    label: str
    score: float


class GLiNERResponse(BaseModel):
    """Backward-compatible response model."""

    entities: list[Entity]


class ProcessingRules(BaseModel):
    deduplicate: bool = True
    normalize_whitespace: bool = True
    lowercase_labels: bool = True
    value_normalizers: dict[str, NormalizationMode] = Field(default_factory=dict)


class ProcessingOverrides(BaseModel):
    deduplicate: bool | None = None
    normalize_whitespace: bool | None = None
    lowercase_labels: bool | None = None
    value_normalizers: dict[str, NormalizationMode] | None = None


class ExtractionTemplate(BaseModel):
    key: str
    name: str
    description: str
    labels: list[str] = Field(..., min_items=1)
    processing: ProcessingRules = Field(default_factory=ProcessingRules)


class GLiNERConfiguredRequest(BaseModel):
    text: str = Field(..., min_length=1)
    use_case: str | None = None
    labels: list[str] | None = Field(default=None, min_items=1)
    processing_overrides: ProcessingOverrides | None = None


class GLiNERConfiguredResponse(BaseModel):
    use_case: str
    labels: list[str]
    processing: ProcessingRules
    entities: list[Entity]
    grouped_entities: dict[str, list[str]]


class GLiNERUseCaseInfo(BaseModel):
    key: str
    name: str
    description: str
    labels: list[str]


class GLiNERUseCaseListResponse(BaseModel):
    use_cases: list[GLiNERUseCaseInfo]
