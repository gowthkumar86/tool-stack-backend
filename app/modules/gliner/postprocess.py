import re
from typing import Any

from app.modules.gliner.schemas import Entity, ProcessingRules


_WHITESPACE_PATTERN = re.compile(r"\s+")


def _normalize_text(value: str, label: str, rules: ProcessingRules) -> str:
    normalized = value.strip()

    if rules.normalize_whitespace:
        normalized = _WHITESPACE_PATTERN.sub(" ", normalized)

    mode = rules.value_normalizers.get(label)
    if mode == "lower":
        normalized = normalized.lower()
    elif mode == "upper":
        normalized = normalized.upper()
    elif mode == "title":
        normalized = normalized.title()

    return normalized


def structure_entities(
    raw_entities: list[dict[str, Any]],
    expected_labels: list[str],
    rules: ProcessingRules,
) -> tuple[list[Entity], dict[str, list[str]]]:
    normalized_labels = [label.lower() if rules.lowercase_labels else label for label in expected_labels]
    grouped: dict[str, list[str]] = {label: [] for label in normalized_labels}

    dedup_index: dict[tuple[str, str], Entity] = {}
    dedup_order: list[tuple[str, str]] = []
    processed_entities: list[Entity] = []

    for item in raw_entities:
        raw_label = str(item.get("label", "")).strip()
        raw_text = str(item.get("text", "")).strip()
        raw_score = float(item.get("score", 0.0))

        if not raw_label or not raw_text:
            continue

        label = raw_label.lower() if rules.lowercase_labels else raw_label
        text = _normalize_text(raw_text, label, rules)
        if not text:
            continue

        entity = Entity(text=text, label=label, score=raw_score)

        if rules.deduplicate:
            dedup_key = (label, text.casefold())
            existing = dedup_index.get(dedup_key)
            if existing is None:
                dedup_index[dedup_key] = entity
                dedup_order.append(dedup_key)
            elif entity.score > existing.score:
                dedup_index[dedup_key] = entity
        else:
            processed_entities.append(entity)

    if rules.deduplicate:
        processed_entities = [dedup_index[key] for key in dedup_order]

    for entity in processed_entities:
        grouped.setdefault(entity.label, [])
        grouped[entity.label].append(entity.text)

    return processed_entities, grouped
