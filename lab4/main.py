from pathlib import Path

from image_io import (
    INPUT_COLOR_DIR,
    INPUT_SEMITONE_DIR,
    OUTPUT_PATHS,
    ensure_directories,
    get_image_files,
    read_color_image,
    read_grayscale_image,
    save_image,
    make_output_name,
)
from processing import to_grayscale, normalize_to_uint8, binarize
from edge_kayyali import apply_kayyali


DEFAULT_THRESHOLD = 40


def process_color_images(threshold: int = DEFAULT_THRESHOLD) -> None:
    files = get_image_files(INPUT_COLOR_DIR)

    for image_path in files:
        image_bgr = read_color_image(image_path)
        if image_bgr is None:
            print(f"[ERROR] Не удалось прочитать цветное изображение: {image_path}")
            continue

        gray = to_grayscale(image_bgr)
        gx, gy, gradient = apply_kayyali(gray)

        gx_norm = normalize_to_uint8(gx)
        gy_norm = normalize_to_uint8(gy)
        gradient_norm = normalize_to_uint8(gradient)
        binary = binarize(gradient_norm, threshold)

        stem = image_path.stem

        save_image(OUTPUT_PATHS["color"]["gray"] / make_output_name(stem, "gray"), gray)
        save_image(OUTPUT_PATHS["color"]["gx"] / make_output_name(stem, "gx"), gx_norm)
        save_image(OUTPUT_PATHS["color"]["gy"] / make_output_name(stem, "gy"), gy_norm)
        save_image(
            OUTPUT_PATHS["color"]["gradient"] / make_output_name(stem, "gradient"),
            gradient_norm,
        )
        save_image(
            OUTPUT_PATHS["color"]["binary"]
            / make_output_name(stem, "binary", threshold),
            binary,
        )

        print(f"[OK] Color processed: {image_path.name}")


def process_semitone_images(threshold: int = DEFAULT_THRESHOLD) -> None:
    files = get_image_files(INPUT_SEMITONE_DIR)

    for image_path in files:
        gray = read_grayscale_image(image_path)
        if gray is None:
            print(f"[ERROR] Не удалось прочитать полутоновое изображение: {image_path}")
            continue

        gx, gy, gradient = apply_kayyali(gray)

        gx_norm = normalize_to_uint8(gx)
        gy_norm = normalize_to_uint8(gy)
        gradient_norm = normalize_to_uint8(gradient)
        binary = binarize(gradient_norm, threshold)

        stem = image_path.stem

        save_image(
            OUTPUT_PATHS["semitone"]["gray"] / make_output_name(stem, "gray"), gray
        )
        save_image(
            OUTPUT_PATHS["semitone"]["gx"] / make_output_name(stem, "gx"), gx_norm
        )
        save_image(
            OUTPUT_PATHS["semitone"]["gy"] / make_output_name(stem, "gy"), gy_norm
        )
        save_image(
            OUTPUT_PATHS["semitone"]["gradient"] / make_output_name(stem, "gradient"),
            gradient_norm,
        )
        save_image(
            OUTPUT_PATHS["semitone"]["binary"]
            / make_output_name(stem, "binary", threshold),
            binary,
        )

        print(f"[OK] Semitone processed: {image_path.name}")


def main():
    ensure_directories()

    process_color_images()
    process_semitone_images()

    print("\nГотово. Все результаты сохранены в output/.")


if __name__ == "__main__":
    main()
