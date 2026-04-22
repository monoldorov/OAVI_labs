from pathlib import Path
from typing import Iterable

from PIL import ImageFont


def find_existing_font_path(candidates: Iterable[Path]) -> Path:

    checked = []
    for candidate in candidates:
        checked.append(str(candidate))
        if candidate.exists() and candidate.is_file():
            return candidate

    checked_str = "\n".join(checked)
    raise FileNotFoundError(
        "Не найден подходящий TTF-шрифт.\n"
        "Проверьте список FONT_CANDIDATES в config.py.\n"
        "Проверенные пути:\n"
        f"{checked_str}\n\n"
        "Важно: fallback на встроенный tiny bitmap font запрещён."
    )


def load_font(font_path: Path, font_size: int) -> ImageFont.FreeTypeFont:

    try:
        font = ImageFont.truetype(str(font_path), size=font_size)
    except Exception as exc:
        raise RuntimeError(
            f"Не удалось загрузить шрифт '{font_path}'. "
            "Проверьте, что это корректный .ttf файл."
        ) from exc

    return font
