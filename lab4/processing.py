import cv2
import numpy as np


def to_grayscale(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)


def normalize_to_uint8(matrix: np.ndarray) -> np.ndarray:
    matrix = matrix.astype(np.float32)

    min_val = np.min(matrix)
    max_val = np.max(matrix)

    if max_val - min_val < 1e-8:
        return np.zeros_like(matrix, dtype=np.uint8)

    normalized = (matrix - min_val) * 255.0 / (max_val - min_val)
    return normalized.astype(np.uint8)


def binarize(image_uint8: np.ndarray, threshold: int) -> np.ndarray:
    _, binary = cv2.threshold(image_uint8, threshold, 255, cv2.THRESH_BINARY)
    return binary
