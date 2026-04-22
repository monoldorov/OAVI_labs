from __future__ import annotations

import math
import re
import unicodedata
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from PIL import Image, ImageDraw, ImageFont


def make_safe_stem(symbol: str) -> str:

    return symbol


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
            "Проверьте шрифт, размер шрифта или порог."
        )

    return binary_black


def crop_white_margins(binary_black: np.ndarray) -> np.ndarray:

    ys, xs = np.where(binary_black == 1)

    if len(xs) == 0 or len(ys) == 0:
        raise ValueError("Нельзя обрезать пустое изображение.")

    x_min, x_max = int(xs.min()), int(xs.max())
    y_min, y_max = int(ys.min()), int(ys.max())

    cropped = binary_black[y_min : y_max + 1, x_min : x_max + 1]
    return cropped


def save_binary_png(binary_black: np.ndarray, output_path: Path) -> None:

    image_data = np.where(binary_black == 1, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_data, mode="L")
    image.save(output_path)


def compute_profiles(binary_black: np.ndarray) -> tuple[np.ndarray, np.ndarray]:

    profile_x = binary_black.sum(axis=0).astype(int)
    profile_y = binary_black.sum(axis=1).astype(int)
    return profile_x, profile_y


def save_profile_plot(
    values: np.ndarray,
    coordinate_name: str,
    output_path: Path,
    title: str,
) -> None:

    indices = np.arange(len(values), dtype=int)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(indices, values, width=0.95)

    ax.set_title(title)
    ax.set_xlabel(f"{coordinate_name} coordinate")
    ax.set_ylabel("Black pixel count")

    # Только целые подписи
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_xlim(-0.5, len(values) - 0.5)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def _quadrant_slices(height: int, width: int):

    y_mid = height // 2
    x_mid = width // 2

    return {
        "top_left": (slice(0, y_mid), slice(0, x_mid)),
        "top_right": (slice(0, y_mid), slice(x_mid, width)),
        "bottom_left": (slice(y_mid, height), slice(0, x_mid)),
        "bottom_right": (slice(y_mid, height), slice(x_mid, width)),
    }


def compute_scalar_features(
    symbol: str,
    image_file: str,
    binary_black: np.ndarray,
) -> dict[str, Any]:

    height, width = binary_black.shape
    total_area = width * height

    quadrants = _quadrant_slices(height, width)

    quarter_weights: dict[str, int] = {}
    quarter_rel_weights: dict[str, float] = {}

    for name, (ys, xs) in quadrants.items():
        part = binary_black[ys, xs]
        weight = int(part.sum())
        area = int(part.shape[0] * part.shape[1])

        quarter_weights[name] = weight
        quarter_rel_weights[name] = (weight / area) if area > 0 else 0.0

    ys, xs = np.where(binary_black == 1)
    black_mass = int(len(xs))
    if black_mass == 0:
        raise ValueError(f"Символ {symbol!r} после обрезки пустой.")

    x_center = float(xs.mean())
    y_center = float(ys.mean())

    x_center_rel = x_center / (width - 1) if width > 1 else 0.0
    y_center_rel = y_center / (height - 1) if height > 1 else 0.0

    ix = float(np.sum((ys - y_center) ** 2))
    iy = float(np.sum((xs - x_center) ** 2))

    ix_rel = ix / total_area
    iy_rel = iy / total_area

    return {
        "symbol": symbol,
        "codepoint": f"U+{ord(symbol):04X}",
        "image_file": image_file,
        "quarter_top_left_black_mass": quarter_weights["top_left"],
        "quarter_top_right_black_mass": quarter_weights["top_right"],
        "quarter_bottom_left_black_mass": quarter_weights["bottom_left"],
        "quarter_bottom_right_black_mass": quarter_weights["bottom_right"],
        "quarter_top_left_rel_black_mass": quarter_rel_weights["top_left"],
        "quarter_top_right_rel_black_mass": quarter_rel_weights["top_right"],
        "quarter_bottom_left_rel_black_mass": quarter_rel_weights["bottom_left"],
        "quarter_bottom_right_rel_black_mass": quarter_rel_weights["bottom_right"],
        "center_x": x_center,
        "center_y": y_center,
        "center_x_rel": x_center_rel,
        "center_y_rel": y_center_rel,
        "inertia_x": ix,
        "inertia_y": iy,
        "inertia_x_rel": ix_rel,
        "inertia_y_rel": iy_rel,
    }


def csv_columns() -> list[str]:
    return [
        "symbol",
        "codepoint",
        "image_file",
        "quarter_top_left_black_mass",
        "quarter_top_right_black_mass",
        "quarter_bottom_left_black_mass",
        "quarter_bottom_right_black_mass",
        "quarter_top_left_rel_black_mass",
        "quarter_top_right_rel_black_mass",
        "quarter_bottom_left_rel_black_mass",
        "quarter_bottom_right_rel_black_mass",
        "center_x",
        "center_y",
        "center_x_rel",
        "center_y_rel",
        "inertia_x",
        "inertia_y",
        "inertia_x_rel",
        "inertia_y_rel",
    ]


def format_csv_value(value: Any) -> str:

    if isinstance(value, (int, np.integer)):
        return str(int(value))

    if isinstance(value, float):
        if math.isfinite(value):
            text = f"{value:.6f}".rstrip("0").rstrip(".")
            return text if text else "0"
        return str(value)

    return str(value)
