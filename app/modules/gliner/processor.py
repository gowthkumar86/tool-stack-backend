from functools import lru_cache

from gliner import GLiNER


class GLiNERProcessor:
    """Runs entity prediction with a loaded GLiNER model."""

    def __init__(self, model_name: str = "urchade/gliner_base") -> None:
        self._model = GLiNER.from_pretrained(model_name)

    def predict_entities(self, text: str, labels: list[str]) -> list[dict]:
        return self._model.predict_entities(text, labels)


@lru_cache
def get_gliner_processor() -> GLiNERProcessor:
    # Cache model initialization so we load it once per process.
    return GLiNERProcessor()
