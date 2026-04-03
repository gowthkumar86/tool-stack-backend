from functools import lru_cache
from pathlib import Path

from gliner import GLiNER

MODEL_DIR = Path(__file__).resolve().parents[3] / "models" / "gliner_small"


class GLiNERProcessor:
    """Runs entity prediction with a loaded GLiNER model."""

    def __init__(self, model_path: Path = MODEL_DIR) -> None:
        if not model_path.exists():
            raise RuntimeError(
                "GLiNER model directory is missing. Run `python download_model.py` during build."
            )
        self._model = GLiNER.from_pretrained(str(model_path))

    def predict_entities(self, text: str, labels: list[str]) -> list[dict]:
        return self._model.predict_entities(text, labels)


@lru_cache
def get_gliner_processor() -> GLiNERProcessor:
    # Cache model initialization so we load it once per process.
    return GLiNERProcessor()
