from typing import Tuple

import numpy as np


def compute_histogram(
    gray_uint8: np.ndarray, bins: int = 256
) -> Tuple[np.ndarray, np.ndarray]:

    hist, bin_edges = np.histogram(gray_uint8.flatten(), bins=bins, range=(0, 256))
    return hist, bin_edges
