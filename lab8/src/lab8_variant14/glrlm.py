from typing import Dict, List, Tuple

import numpy as np


def quantize_image(gray_uint8: np.ndarray, levels: int) -> np.ndarray:

    gray = gray_uint8.astype(np.float32)
    quantized = np.floor(gray * levels / 256.0).astype(np.int32)
    quantized = np.clip(quantized, 0, levels - 1)
    return quantized


def _extract_runs_from_direction(
    image: np.ndarray,
    dy: int,
    dx: int,
) -> List[Tuple[int, int]]:

    h, w = image.shape
    runs: List[Tuple[int, int]] = []

    start_points = []

    if (dy, dx) == (0, 1):  # вправо
        for y in range(h):
            start_points.append((y, 0))

    elif (dy, dx) == (-1, 1):  # вправо-вверх
        for y in range(h):
            start_points.append((y, 0))
        for x in range(1, w):
            start_points.append((h - 1, x))

    elif (dy, dx) == (1, 0):  # вниз
        for x in range(w):
            start_points.append((0, x))

    elif (dy, dx) == (1, -1):  # влево-вниз
        for x in range(w):
            start_points.append((0, x))
        for y in range(1, h):
            start_points.append((y, w - 1))

    else:
        raise ValueError(f"Unsupported direction: {(dy, dx)}")

    for sy, sx in start_points:
        line_values = []
        y, x = sy, sx

        while 0 <= y < h and 0 <= x < w:
            line_values.append(int(image[y, x]))
            y += dy
            x += dx

        if not line_values:
            continue

        current_value = line_values[0]
        current_run_length = 1

        for value in line_values[1:]:
            if value == current_value:
                current_run_length += 1
            else:
                runs.append((current_value, current_run_length))
                current_value = value
                current_run_length = 1

        runs.append((current_value, current_run_length))

    return runs


def build_glrlm(
    gray_uint8: np.ndarray,
    levels: int,
    directions: List[Tuple[int, int]],
) -> np.ndarray:

    quantized = quantize_image(gray_uint8, levels=levels)
    h, w = quantized.shape
    max_run_length = max(h, w)

    matrix = np.zeros((levels, max_run_length), dtype=np.float64)

    for dy, dx in directions:
        runs = _extract_runs_from_direction(quantized, dy=dy, dx=dx)
        for gray_level, run_length in runs:
            matrix[gray_level, run_length - 1] += 1.0

    return matrix


def compute_glrlm_features(glrlm: np.ndarray) -> Dict[str, float]:

    total_runs = np.sum(glrlm)

    if total_runs == 0:
        return {
            "SRE": 0.0,
            "LRE": 0.0,
        }

    p = glrlm / total_runs

    levels_count, run_lengths_count = p.shape
    run_lengths = np.arange(1, run_lengths_count + 1, dtype=np.float64)

    r = run_lengths[np.newaxis, :]

    sre = np.sum(p / (r**2))
    lre = np.sum(p * (r**2))

    return {
        "SRE": float(sre),
        "LRE": float(lre),
    }
