from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def save_histogram_plot(
    hist: np.ndarray,
    save_path: Path,
    title: str,
) -> None:
    plt.figure(figsize=(8, 4))
    plt.bar(np.arange(len(hist)), hist, width=1.0)
    plt.title(title)
    plt.xlabel("Яркость")
    plt.ylabel("Количество пикселей")
    plt.xlim(0, 255)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def save_matrix_image(
    matrix: np.ndarray,
    save_path: Path,
    title: str,
    use_log_normalization: bool = True,
) -> None:

    arr = matrix.astype(np.float64)

    if use_log_normalization:
        arr = np.log1p(arr)

    max_val = np.max(arr)
    if max_val > 0:
        arr = arr / max_val

    arr_uint8 = np.clip(arr * 255.0, 0, 255).astype(np.uint8)

    plt.figure(figsize=(8, 5))
    plt.imshow(arr_uint8, cmap="gray", aspect="auto")
    plt.title(title)
    plt.xlabel("Длина серии")
    plt.ylabel("Уровень яркости")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def save_gray_image(gray_uint8: np.ndarray, save_path: Path) -> None:
    Image.fromarray(gray_uint8.astype(np.uint8), mode="L").save(save_path)
