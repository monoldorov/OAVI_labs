from os import path
from PIL import Image
import numpy as np


PROJECT_DIR = path.dirname(path.abspath(__file__))
SOURCE_FOLDER = path.join(PROJECT_DIR, "pictures_src")


def load_image(image_filename: str) -> np.ndarray:
    full_path = path.join(SOURCE_FOLDER, image_filename)
    image = Image.open(full_path).convert("RGB")
    return np.asarray(image, dtype=np.uint8)


def get_new_size(old_size: tuple[int, int], scale_value, size_transform):
    height, width = old_size
    return size_transform(height, scale_value), size_transform(width, scale_value)


def nearest_resample(
    image_array: np.ndarray, scale_value, size_transform, coord_transform
) -> np.ndarray:
    source_height, source_width = image_array.shape[:2]
    target_height, target_width = get_new_size(
        (source_height, source_width), scale_value, size_transform
    )

    result = np.empty(
        (target_height, target_width, image_array.shape[2]), dtype=np.uint8
    )

    for row in range(target_height):
        for col in range(target_width):
            source_row = min(coord_transform(row, scale_value), source_height - 1)
            source_col = min(coord_transform(col, scale_value), source_width - 1)
            result[row, col] = image_array[source_row, source_col]

    return result


def resample_in_two_steps(
    image_array: np.ndarray, up_factor: int, down_factor: int
) -> np.ndarray:
    first_step = nearest_resample(
        image_array,
        up_factor,
        lambda size, factor: size * factor,
        lambda coord, factor: int(round(coord / factor)),
    )

    second_step = nearest_resample(
        first_step,
        down_factor,
        lambda size, factor: int(round(size / factor)),
        lambda coord, factor: coord * factor,
    )

    return second_step


def image_to_np_array(image_name: str) -> np.ndarray:
    return load_image(image_name)


def one_step_resampling(img: np.ndarray, factor: float, f1, f2) -> np.ndarray:
    return nearest_resample(img, factor, f1, f2)


def two_step_resampling(
    img: np.ndarray, numerator: int, denominator: int
) -> np.ndarray:
    return resample_in_two_steps(img, numerator, denominator)


if __name__ == "__main__":
    pass
