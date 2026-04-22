from pathlib import Path
from typing import Iterable

from PIL import ImageFont


def find_existing_font_path(candidates: Iterable[Path]) -> Path:
    checked = []
    for candidate in candidates:
        checked.append(str(candidate))
        if candidate.exists() and candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "Не найден подходящий TTF-шрифт.\n"
        "Проверь FONT_CANDIDATES в config.py.\n"
        "Проверенные пути:\n" + "\n".join(checked)
    )


def load_font(font_path: Path, font_size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(font_path), size=font_size)
    except Exception as exc:
        raise RuntimeError(f"Не удалось загрузить шрифт: {font_path}") from exc