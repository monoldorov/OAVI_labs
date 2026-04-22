from pathlib import Path
from typing import List

from PIL import Image

from .config import ALL_OUTPUT_DIRS, ALLOWED_EXTENSIONS, INPUT_DIR


def ensure_directories() -> None:
    for directory in ALL_OUTPUT_DIRS:
        directory.mkdir(parents=True, exist_ok=True)


def collect_input_images() -> List[Path]:
    if not INPUT_DIR.exists():
        return []

    images = []
    for path in INPUT_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            images.append(path)

    return sorted(images)


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")
