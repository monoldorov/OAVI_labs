import numpy as np


def integral_image(img: np.ndarray) -> np.ndarray:
    img64 = img.astype(np.int64)
    return img64.cumsum(axis=0).cumsum(axis=1)


def rect_sum(ii: np.ndarray, top: int, left: int, bottom: int, right: int) -> int:
    total = ii[bottom, right]

    if top > 0:
        total -= ii[top - 1, right]
    if left > 0:
        total -= ii[bottom, left - 1]
    if top > 0 and left > 0:
        total += ii[top - 1, left - 1]

    return int(total)
