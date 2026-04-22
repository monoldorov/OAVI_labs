from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


def horizontal_profile(binary_black: np.ndarray) -> np.ndarray:

    return binary_black.sum(axis=1).astype(int)


def vertical_profile(binary_black: np.ndarray) -> np.ndarray:

    return binary_black.sum(axis=0).astype(int)


def thin_profile(values: np.ndarray, empty_threshold: int) -> np.ndarray:

    result = values.copy()
    result[result <= empty_threshold] = 0
    return result


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

    ax.xaxis.set_major_locator(MaxNLocator(nbins=12, integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

    ax.set_xlim(-0.5, len(values) - 0.5)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
