from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def load_bmp_as_binary_black(image_path: Path, threshold: int) -> np.ndarray:

    image = Image.open(image_path).convert("L")
    gray = np.array(image, dtype=np.uint8)
    binary_black = (gray < threshold).astype(np.uint8)

    if int(binary_black.sum()) == 0:
        raise ValueError(f"Во входном изображении нет черных пикселей: {image_path}")

    return binary_black


def save_binary_png(binary_black: np.ndarray, output_path: Path) -> None:
    image_data = np.where(binary_black == 1, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_data, mode="L")
    image.save(output_path)


def save_binary_bmp(binary_black: np.ndarray, output_path: Path) -> None:
    image_data = np.where(binary_black == 1, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_data, mode="L")
    image.save(output_path)


def crop_white_margins(binary_black: np.ndarray) -> np.ndarray:
    ys, xs = np.where(binary_black == 1)

    if len(xs) == 0 or len(ys) == 0:
        raise ValueError("Нельзя обрезать пустое изображение.")

    x_min, x_max = int(xs.min()), int(xs.max())
    y_min, y_max = int(ys.min()), int(ys.max())

    return binary_black[y_min : y_max + 1, x_min : x_max + 1]


def render_symbol_to_binary(
    symbol: str,
    font: ImageFont.FreeTypeFont,
    canvas_size: tuple[int, int],
    threshold: int,
) -> np.ndarray:

    width, height = canvas_size
    image = Image.new("L", (width, height), color=255)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), symbol, font=font)
    if bbox is None:
        raise ValueError(f"Не удалось вычислить bbox для символа {symbol!r}")

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) / 2 - bbox[0]
    y = (height - text_h) / 2 - bbox[1]

    draw.text((x, y), symbol, fill=0, font=font)

    gray = np.array(image, dtype=np.uint8)
    binary_black = (gray < threshold).astype(np.uint8)

    if int(binary_black.sum()) == 0:
        raise ValueError(
            f"После бинаризации символ {symbol!r} пустой. "
            "Проверьте шрифт, размер или порог."
        )

    return binary_black


def build_phrase_image_from_symbols(
    phrase: str,
    symbol_images: dict[str, np.ndarray],
    letter_spacing: int,
    space_width: int,
    line_padding: int,
) -> np.ndarray:

    tokens: list[tuple[str, np.ndarray | None]] = []
    for char in phrase:
        if char == " ":
            tokens.append(("space", None))
        else:
            if char not in symbol_images:
                raise ValueError(f"Символ {char!r} отсутствует в symbol_images.")
            tokens.append(("symbol", symbol_images[char]))

    symbol_imgs = [img for kind, img in tokens if kind == "symbol" and img is not None]
    if not symbol_imgs:
        raise ValueError("Фраза не содержит символов для сборки.")

    max_height = max(img.shape[0] for img in symbol_imgs)

    total_width = 2 * line_padding
    for i, (kind, img) in enumerate(tokens):
        if kind == "space":
            total_width += space_width
        else:
            assert img is not None
            total_width += img.shape[1]
            if i < len(tokens) - 1 and tokens[i + 1][0] == "symbol":
                total_width += letter_spacing

    total_height = max_height + 2 * line_padding
    line = np.zeros((total_height, total_width), dtype=np.uint8)

    x_cursor = line_padding
    for i, (kind, img) in enumerate(tokens):
        if kind == "space":
            x_cursor += space_width
            continue

        assert img is not None
        h, w = img.shape
        y_offset = line_padding + (max_height - h) // 2
        line[y_offset : y_offset + h, x_cursor : x_cursor + w] = img
        x_cursor += w

        if i < len(tokens) - 1 and tokens[i + 1][0] == "symbol":
            x_cursor += letter_spacing

    return crop_white_margins(line)


def save_boxes_visualization(
    binary_black: np.ndarray,
    boxes: list[tuple[int, int, int, int]],
    output_path: Path,
) -> None:

    image_data = np.where(binary_black == 1, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_data, mode="L").convert("RGB")
    draw = ImageDraw.Draw(image)

    for x1, y1, x2, y2 in boxes:
        draw.rectangle((x1, y1, x2, y2), outline=(255, 0, 0), width=1)

    image.save(output_path)


def save_crop(
    binary_black: np.ndarray, box: tuple[int, int, int, int], output_path: Path
) -> None:
    x1, y1, x2, y2 = box
    crop = binary_black[y1 : y2 + 1, x1 : x2 + 1]
    save_binary_png(crop, output_path)
