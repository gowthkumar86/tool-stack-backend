from typing import Any

from app.modules.gliner.postprocess import structure_entities
from app.modules.gliner.processor import get_gliner_processor
from app.modules.gliner.schemas import (
    GLiNERConfiguredResponse,
    GLiNERUseCaseInfo,
    ProcessingOverrides,
    ProcessingRules,
)
from app.modules.gliner.templates import get_use_case_template, list_use_case_templates


def extract_entities(text: str, labels: list[str]) -> list[dict[str, Any]]:
    """Backward-compatible raw extraction used by existing endpoint/callers."""

    processor = get_gliner_processor()
    entities = processor.predict_entities(text, labels)

    return [
        {
            "text": entity["text"],
            "label": entity["label"],
            "score": entity["score"],
        }
        for entity in entities
    ]


def _merge_processing_rules(
    base_rules: ProcessingRules,
    overrides: ProcessingOverrides | None,
) -> ProcessingRules:
    if overrides is None:
        return base_rules

    value_normalizers = dict(base_rules.value_normalizers)
    if overrides.value_normalizers is not None:
        value_normalizers.update(overrides.value_normalizers)

    return ProcessingRules(
        deduplicate=base_rules.deduplicate if overrides.deduplicate is None else overrides.deduplicate,
        normalize_whitespace=(
            base_rules.normalize_whitespace
            if overrides.normalize_whitespace is None
            else overrides.normalize_whitespace
        ),
        lowercase_labels=(
            base_rules.lowercase_labels
            if overrides.lowercase_labels is None
            else overrides.lowercase_labels
        ),
        value_normalizers=value_normalizers,
    )


def _resolve_runtime_config(
    use_case: str | None,
    labels: list[str] | None,
    processing_overrides: ProcessingOverrides | None,
) -> tuple[str, list[str], ProcessingRules]:
    template = get_use_case_template(use_case) if use_case else None

    if use_case and template is None:
        raise ValueError(f"Unknown use case '{use_case}'.")

    resolved_labels = labels or (template.labels if template else None)
    if not resolved_labels:
        raise ValueError("Provide either 'use_case' or a non-empty 'labels' list.")

    base_rules = template.processing if template else ProcessingRules()
    runtime_rules = _merge_processing_rules(base_rules, processing_overrides)

    resolved_use_case = template.key if template else "custom"
    return resolved_use_case, resolved_labels, runtime_rules


def extract_entities_configured(
    text: str,
    use_case: str | None = None,
    labels: list[str] | None = None,
    processing_overrides: ProcessingOverrides | None = None,
) -> GLiNERConfiguredResponse:
    resolved_use_case, resolved_labels, runtime_rules = _resolve_runtime_config(
        use_case=use_case,
        labels=labels,
        processing_overrides=processing_overrides,
    )

    raw_entities = extract_entities(text, resolved_labels)
    entities, grouped_entities = structure_entities(raw_entities, resolved_labels, runtime_rules)

    return GLiNERConfiguredResponse(
        use_case=resolved_use_case,
        labels=resolved_labels,
        processing=runtime_rules,
        entities=entities,
        grouped_entities=grouped_entities,
    )


def list_use_cases() -> list[GLiNERUseCaseInfo]:
    return [
        GLiNERUseCaseInfo(
            key=template.key,
            name=template.name,
            description=template.description,
            labels=template.labels,
        )
        for template in list_use_case_templates()
    ]
