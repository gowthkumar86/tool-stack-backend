from pathlib import Path

from huggingface_hub import snapshot_download

MODEL_ID = "urchade/gliner_small-v1"
TARGET_DIR = Path(__file__).resolve().parent / "models" / "gliner_small"


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=MODEL_ID, local_dir=str(TARGET_DIR))
    print(f"GLiNER model downloaded to: {TARGET_DIR}")


if __name__ == "__main__":
    main()
