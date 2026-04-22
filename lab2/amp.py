import numpy as np
from semitone import semitone
from integral import integral_image, rect_sum


def adaptive_monochrome_threshold(
    image: np.ndarray, window_size: int = 5
) -> np.ndarray:

    if window_size <= 0 or window_size % 2 == 0:
        raise ValueError("Размер окна должен быть положительным нечетным числом.")

    if image.ndim == 3:
        gray = semitone(image)
    else:
        gray = image.astype(np.uint8)

    h, w = gray.shape
    result = np.zeros((h, w), dtype=np.uint8)
    ii = integral_image(gray)

    r = window_size // 2

    for y in range(h):
        top = max(0, y - r)
        bottom = min(h - 1, y + r)

        for x in range(w):
            left = max(0, x - r)
            right = min(w - 1, x + r)

            area = (bottom - top + 1) * (right - left + 1)
            local_sum = rect_sum(ii, top, left, bottom, right)
            local_avg = local_sum / area

            result[y, x] = 255 if gray[y, x] >= local_avg else 0

    return result
