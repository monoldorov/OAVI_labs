from PIL import Image
import numpy as np
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
SRC_DIR = path.join(BASE_DIR, "pictures_src")
SEMITONE_RESULT_DIR = path.join(BASE_DIR, "pictures_results_semitone")
BINARY_RESULT_DIR = path.join(BASE_DIR, "pictures_results_binary")


def image_to_np_array(image_name: str) -> np.ndarray:
    img_src = Image.open(path.join(SRC_DIR, image_name)).convert("RGB")
    return np.array(img_src, dtype=np.uint8)


def semitone(img: np.ndarray) -> np.ndarray:
    if img.ndim == 2:
        return img.astype(np.uint8)

    y = (
        0.3 * img[:, :, 0] +
        0.59 * img[:, :, 1] +
        0.11 * img[:, :, 2]
    )
    return y.astype(np.uint8)


def to_semitone(image_name: str) -> Image.Image:
    img = image_to_np_array(image_name)
    gray = semitone(img)
    return Image.fromarray(gray, mode="L")