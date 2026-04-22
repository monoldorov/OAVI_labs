from pathlib import Path
from typing import Dict, List

import csv
import numpy as np

from .config import (
    COLOR_CONTRAST_DIR,
    CONTRAST_GRAY_DIR,
    GLRLM_DIRECTIONS,
    GLRLM_LEVELS,
    GRAY_DIR,
    HIST_AFTER_DIR,
    HIST_BEFORE_DIR,
    MATRIX_AFTER_DIR,
    MATRIX_BEFORE_DIR,
    TABLES_DIR,
)
from .contrast import logarithmic_contrast_transform
from .glrlm import build_glrlm, compute_glrlm_features
from .histogram import compute_histogram
from .hsl import (
    hsl_arrays_to_rgb_image,
    lightness_to_uint8_image,
    rgb_image_to_hsl_arrays,
)
from .io_utils import collect_input_images, ensure_directories, load_image
from .visualization import save_gray_image, save_histogram_plot, save_matrix_image


def process_all_images() -> None:
    ensure_directories()
    image_paths = collect_input_images()

    if not image_paths:
        print("В папке input/images нет изображений.")
        return

    rows: List[Dict[str, str]] = []

    for image_path in image_paths:
        print(f"Обрабатывается: {image_path.name}")
        row = process_single_image(image_path)
        rows.append(row)

    save_results_table(rows)
    print("Готово.")


def process_single_image(image_path: Path) -> Dict[str, str]:

    image = load_image(image_path)
    stem = image_path.stem

    h, s, l = rgb_image_to_hsl_arrays(image)

    gray_before_uint8 = np.clip(l * 255.0, 0, 255).astype(np.uint8)
    save_gray_image(gray_before_uint8, GRAY_DIR / f"{stem}_gray.png")

    gray_after = logarithmic_contrast_transform(gray_before_uint8.astype(np.float32))
    gray_after_uint8 = np.clip(gray_after, 0, 255).astype(np.uint8)
    save_gray_image(gray_after_uint8, CONTRAST_GRAY_DIR / f"{stem}_contrast_gray.png")

    l_after = gray_after_uint8.astype(np.float32) / 255.0
    color_after = hsl_arrays_to_rgb_image(h, s, l_after)
    color_after.save(COLOR_CONTRAST_DIR / f"{stem}_color_contrast.png")

    hist_before, _ = compute_histogram(gray_before_uint8)
    hist_after, _ = compute_histogram(gray_after_uint8)

    save_histogram_plot(
        hist_before,
        HIST_BEFORE_DIR / f"{stem}_hist_before.png",
        title=f"Histogram before: {stem}",
    )
    save_histogram_plot(
        hist_after,
        HIST_AFTER_DIR / f"{stem}_hist_after.png",
        title=f"Histogram after: {stem}",
    )

    glrlm_before = build_glrlm(
        gray_uint8=gray_before_uint8,
        levels=GLRLM_LEVELS,
        directions=GLRLM_DIRECTIONS,
    )
    glrlm_after = build_glrlm(
        gray_uint8=gray_after_uint8,
        levels=GLRLM_LEVELS,
        directions=GLRLM_DIRECTIONS,
    )

    save_matrix_image(
        glrlm_before,
        MATRIX_BEFORE_DIR / f"{stem}_glrlm_before.png",
        title=f"GLRLM before: {stem}",
        use_log_normalization=True,
    )
    save_matrix_image(
        glrlm_after,
        MATRIX_AFTER_DIR / f"{stem}_glrlm_after.png",
        title=f"GLRLM after: {stem}",
        use_log_normalization=True,
    )

    features_before = compute_glrlm_features(glrlm_before)
    features_after = compute_glrlm_features(glrlm_after)

    return {
        "image_name": image_path.name,
        "SRE_before": f"{features_before['SRE']:.6f}",
        "LRE_before": f"{features_before['LRE']:.6f}",
        "SRE_after": f"{features_after['SRE']:.6f}",
        "LRE_after": f"{features_after['LRE']:.6f}",
    }


def save_results_table(rows: List[Dict[str, str]]) -> None:
    save_path = TABLES_DIR / "features_comparison.csv"
    fieldnames = [
        "image_name",
        "SRE_before",
        "LRE_before",
        "SRE_after",
        "LRE_after",
    ]

    with open(save_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
