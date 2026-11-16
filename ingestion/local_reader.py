
import json
from pathlib import Path


def load_json(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
