from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


def compute_symbol_features(binary_black: np.ndarray) -> dict[str, float]:
    """
    1 = черный пиксель, 0 = белый
    """
    h, w = binary_black.shape
    weight = float(binary_black.sum())

    if weight == 0:
        raise ValueError("Пустой символ: вес равен 0.")

    ys, xs = np.where(binary_black == 1)

    center_x = float(xs.mean())
    center_y = float(ys.mean())

    # Нормированные координаты центра тяжести
    center_x_rel = center_x / (w - 1) if w > 1 else 0.0
    center_y_rel = center_y / (h - 1) if h > 1 else 0.0

    # Осевые моменты инерции
    ix = float(((ys - center_y) ** 2).sum())
    iy = float(((xs - center_x) ** 2).sum())

    area = float(w * h)
    weight_rel = weight / area if area > 0 else 0.0
    ix_rel = ix / area if area > 0 else 0.0
    iy_rel = iy / area if area > 0 else 0.0

    return {
        "width": float(w),
        "height": float(h),
        "weight": weight,
        "weight_rel": weight_rel,
        "center_x": center_x,
        "center_y": center_y,
        "center_x_rel": center_x_rel,
        "center_y_rel": center_y_rel,
        "ix": ix,
        "iy": iy,
        "ix_rel": ix_rel,
        "iy_rel": iy_rel,
    }


def save_reference_features_csv(
    rows: list[dict[str, object]],
    output_path: Path,
) -> None:
    if not rows:
        raise ValueError("Нет данных для сохранения в CSV.")

    columns = list(rows[0].keys())

    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([row[col] for col in columns])