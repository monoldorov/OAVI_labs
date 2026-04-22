from os import path
from PIL import Image
import numpy as np

from resampling import image_to_np_array, one_step_resampling, two_step_resampling


CURRENT_DIR = path.dirname(path.abspath(__file__))
RESULT_DIR = path.join(CURRENT_DIR, "pictures_results_2")


AVAILABLE_IMAGES = {"Жесть": "zhest.png"}

AVAILABLE_OPERATIONS = {
    "Интерполяция": "interpolation",
    "Децимация": "decimation",
    "Двухпроходная передискретизация": "two_pass",
    "Однопроходная передискретизация": "one_pass",
}


def choose_from_menu(options: dict, title: str):
    print(title)

    keys = list(options.keys())
    for index, item in enumerate(keys, start=1):
        print(f"{index} - {item}")

    while True:
        try:
            choice = int(input("> ").strip())
            if 1 <= choice <= len(keys):
                selected_key = keys[choice - 1]
                return options[selected_key]
            print("Введите корректное значение")
        except ValueError:
            print("Введите корректное значение")


def read_number(cast_type, message: str, min_value=None, max_value=None):
    print(message)

    while True:
        try:
            value = cast_type(input("> ").strip())

            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError

            return value
        except ValueError:
            print("Введите корректное значение")


def make_one_pass_result(img: np.ndarray, scale, size_rule, index_rule) -> Image.Image:
    resized = one_step_resampling(img, scale, size_rule, index_rule)
    resized = resized.astype(np.uint8)
    return Image.fromarray(resized, "RGB")


def ask_output_filename():
    print(
        "Введите название сохраненного изображения (оставьте пустым, чтобы не сохранять)"
    )
    filename = input("> ").strip()

    if not filename:
        return ""

    if "." not in filename:
        filename += ".png"

    return filename


def save_result(image: Image.Image, filename: str):
    if not filename:
        return

    save_path = path.join(RESULT_DIR, filename)
    image.save(save_path)
    print(f"Сохранено: {save_path}")


def run_interpolation(img: np.ndarray) -> Image.Image:
    factor = read_number(int, "Введите целый коэффициент растяжения", min_value=1)
    return make_one_pass_result(
        img, factor, lambda size, k: size * k, lambda coord, k: int(round(coord / k))
    )


def run_decimation(img: np.ndarray) -> Image.Image:
    factor = read_number(int, "Введите целый коэффициент сжатия", min_value=1)
    return make_one_pass_result(
        img, factor, lambda size, k: int(round(size / k)), lambda coord, k: coord * k
    )


def run_two_pass(img: np.ndarray) -> Image.Image:
    numerator = read_number(int, "Введите целый коэффициент растяжения", min_value=1)
    denominator = read_number(int, "Введите целый коэффициент сжатия", min_value=1)

    result = two_step_resampling(img, numerator, denominator).astype(np.uint8)
    return Image.fromarray(result, "RGB")


def run_one_pass(img: np.ndarray) -> Image.Image:
    factor = read_number(
        float, "Введите дробный коэффициент растяжения/сжатия", min_value=0.01
    )
    return make_one_pass_result(
        img,
        factor,
        lambda size, k: int(round(size * k)),
        lambda coord, k: int(round(coord / k)),
    )


def main():
    selected_image_name = choose_from_menu(AVAILABLE_IMAGES, "Выберите изображение:")
    source_img = image_to_np_array(selected_image_name)

    selected_mode = choose_from_menu(AVAILABLE_OPERATIONS, "Выберите операцию:")

    if selected_mode == "interpolation":
        output_img = run_interpolation(source_img)

    elif selected_mode == "decimation":
        output_img = run_decimation(source_img)

    elif selected_mode == "two_pass":
        output_img = run_two_pass(source_img)

    elif selected_mode == "one_pass":
        output_img = run_one_pass(source_img)

    else:
        return

    output_name = ask_output_filename()
    save_result(output_img, output_name)


if __name__ == "__main__":
    main()
