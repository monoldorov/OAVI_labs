from __future__ import annotations

import numpy as np


def horizontal_profile(binary_black: np.ndarray) -> np.ndarray:
    return binary_black.sum(axis=1).astype(int)


def vertical_profile(binary_black: np.ndarray) -> np.ndarray:
    return binary_black.sum(axis=0).astype(int)


def thin_profile(values: np.ndarray, empty_threshold: int) -> np.ndarray:
    result = values.copy()
    result[result <= empty_threshold] = 0
    return result


def _find_nonzero_runs(values: np.ndarray) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start = None

    for i, value in enumerate(values):
        if value > 0 and start is None:
            start = i
        elif value == 0 and start is not None:
            runs.append((start, i - 1))
            start = None

    if start is not None:
        runs.append((start, len(values) - 1))

    return runs


def find_text_row_bounds(binary_black: np.ndarray, empty_threshold: int) -> tuple[int, int]:
    h_profile = thin_profile(horizontal_profile(binary_black), empty_threshold)
    runs = _find_nonzero_runs(h_profile)
    if not runs:
        raise ValueError("Не удалось найти строку текста.")
    return max(runs, key=lambda pair: pair[1] - pair[0] + 1)


def segment_symbols_in_line(
    binary_black: np.ndarray,
    horizontal_empty_threshold: int,
    vertical_empty_threshold: int,
    min_symbol_width: int,
    min_symbol_height: int,
) -> list[tuple[int, int, int, int]]:
    y1, y2 = find_text_row_bounds(binary_black, horizontal_empty_threshold)
    line = binary_black[y1:y2 + 1, :]

    v_profile = thin_profile(vertical_profile(line), vertical_empty_threshold)
    x_runs = _find_nonzero_runs(v_profile)

    boxes: list[tuple[int, int, int, int]] = []

    for x_start, x_end in x_runs:
        if x_end - x_start + 1 < min_symbol_width:
            continue

        symbol_part = line[:, x_start:x_end + 1]
        local_h = horizontal_profile(symbol_part)
        local_runs = _find_nonzero_runs(local_h)
        if not local_runs:
            continue

        local_y1 = min(run[0] for run in local_runs)
        local_y2 = max(run[1] for run in local_runs)

        if local_y2 - local_y1 + 1 < min_symbol_height:
            continue

        boxes.append((x_start, y1 + local_y1, x_end, y1 + local_y2))

    return boxes