from os import path
from PIL import Image
import numpy as np

from semitone import (
    to_semitone,
    image_to_np_array,
    SEMITONE_RESULT_DIR,
    BINARY_RESULT_DIR,
)
from amp import adaptive_monochrome_threshold


def prompt(options: dict):
    keys = list(options.keys())
    for idx, name in enumerate(keys, start=1):
        print(f"{idx} - {name}")

    while True:
        try:
            value = int(input("> "))
            if 1 <= value <= len(keys):
                return options[keys[value - 1]]
        except ValueError:
            pass
        print("Введите корректное значение")


def safe_number_input(lower_bound=None, upper_bound=None):
    while True:
        try:
            value = int(input("> "))
            if lower_bound is not None and value < lower_bound:
                raise ValueError
            if upper_bound is not None and value > upper_bound:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное значение")


def run_amp(img: np.ndarray) -> Image.Image:
    print("Введите нечетный размер окна:")
    while True:
        window_size = safe_number_input(3, 99)
        if window_size % 2 == 1:
            break
        print("Размер окна должен быть нечетным")

    result = adaptive_monochrome_threshold(img, window_size)
    return Image.fromarray(result, "L")


images = {
    "Text": "text.png",
    "Cartoon": "cartoon.png",
    "Photo": "photo.png",
    "X-ray": "x-ray.png",
    "Map": "map.png",
}

operations = {
    "Полутон": "semitone",
    "Бинаризация (вариант 14: АМП с усреднением по окну)": "binary",
}


if __name__ == "__main__":
    print("Выберите изображение:")
    selected_image = prompt(images)
    img = image_to_np_array(selected_image)

    print("Выберите обработку изображения:")
    selected_handle = prompt(operations)

    match selected_handle:
        case "semitone":
            result = to_semitone(selected_image)
            save_dir = SEMITONE_RESULT_DIR

        case "binary":
            result = run_amp(img)
            save_dir = BINARY_RESULT_DIR

        case _:
            raise SystemExit

    print(
        "Введите имя файла для сохранения (например result или result.png / result.bmp)."
    )
    print("Если оставить пустым, файл не сохранится:")
    selected_path = input().strip()

    if selected_path:
        name, ext = path.splitext(selected_path)

        if ext == "":
            selected_path += ".png"
        elif ext.lower() not in [".png", ".bmp"]:
            print("Неизвестное расширение, файл будет сохранен как .png")
            selected_path = name + ".png"

        result.save(path.join(save_dir, selected_path))
        print(f"Файл сохранен: {selected_path}")
