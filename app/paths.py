from pathlib import Path

BASE = Path(__file__).parent          # .../app
PROJECT_ROOT = BASE.parent          # .../ (repo root)

def get_data_path(filename="train.csv"):
    candidate = PROJECT_ROOT / "data" / "raw" / filename
    if candidate.exists():
        return candidate.resolve()

    candidates = [
        PROJECT_ROOT / "data" / filename,
        PROJECT_ROOT / "notebooks" / filename,
        BASE / filename,
        PROJECT_ROOT / filename,
    ]
    for c in candidates:
        if c.exists():
            return c.resolve()

    # devuelve el preferido para que el error sea claro
    return candidate.resolve()

DATA_PATH = get_data_path("train.csv")
