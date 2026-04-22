from pathlib import Path

from io_utils import ensure_directories, list_images, read_grayscale_image, save_image
from morphology import binarize_image, dilate_black_object, dilate_semitone
from difference import xor_difference, abs_difference, enhance_difference

BASE_DIR = Path(__file__).resolve().parent

INPUT_BINARY_DIR = BASE_DIR / "input" / "pictures_binary_src"
INPUT_SEMITONE_DIR = BASE_DIR / "input" / "pictures_semitone_src"

OUTPUT_BINARY_DILATED_DIR = BASE_DIR / "output" / "results_binary_dilated"
OUTPUT_BINARY_DIFF_DIR = BASE_DIR / "output" / "results_binary_diff"

OUTPUT_SEMITONE_DILATED_DIR = BASE_DIR / "output" / "results_semitone_dilated"
OUTPUT_SEMITONE_DIFF_DIR = BASE_DIR / "output" / "results_semitone_diff"


def process_binary_images() -> None:
    images = list_images(INPUT_BINARY_DIR)

    if not images:
        print(f"[INFO] В папке {INPUT_BINARY_DIR} нет изображений.")
        return

    for img_path in images:
        try:
            img = read_grayscale_image(img_path)
            binary = binarize_image(img)
            filtered = dilate_black_object(binary)
            diff = xor_difference(binary, filtered)

            filtered_path = save_image(
                OUTPUT_BINARY_DILATED_DIR, img_path, filtered, "dilated"
            )

            diff_path = save_image(OUTPUT_BINARY_DIFF_DIR, img_path, diff, "xor_diff")

            print(f"[OK] Binary processed: {img_path.name}")
            print(f"     Saved filtered -> {filtered_path}")
            print(f"     Saved diff     -> {diff_path}")

        except Exception as e:
            print(f"[ERROR] Ошибка при обработке {img_path.name}: {e}")


def process_semitone_images() -> None:
    images = list_images(INPUT_SEMITONE_DIR)

    if not images:
        print(f"[INFO] В папке {INPUT_SEMITONE_DIR} нет изображений.")
        return

    for img_path in images:
        try:
            img = read_grayscale_image(img_path)
            filtered = dilate_semitone(img)

            diff = abs_difference(img, filtered)
            diff_enhanced = enhance_difference(diff, factor=10)

            filtered_path = save_image(
                OUTPUT_SEMITONE_DILATED_DIR, img_path, filtered, "dilated"
            )

            diff_path = save_image(OUTPUT_SEMITONE_DIFF_DIR, img_path, diff, "abs_diff")

            diff_enhanced_path = save_image(
                OUTPUT_SEMITONE_DIFF_DIR, img_path, diff_enhanced, "abs_diff_contrast"
            )

            print(f"[OK] Semitone processed: {img_path.name}")
            print(f"     Saved filtered      -> {filtered_path}")
            print(f"     Saved diff          -> {diff_path}")
            print(f"     Saved enhanced diff -> {diff_enhanced_path}")

        except Exception as e:
            print(f"[ERROR] Ошибка при обработке {img_path.name}: {e}")


def main() -> None:
    ensure_directories(
        [
            OUTPUT_BINARY_DILATED_DIR,
            OUTPUT_BINARY_DIFF_DIR,
            OUTPUT_SEMITONE_DILATED_DIR,
            OUTPUT_SEMITONE_DIFF_DIR,
        ]
    )

    process_binary_images()
    process_semitone_images()

    print("\nГотово. Все результаты сохранены автоматически в нужные папки.")


if __name__ == "__main__":
    main()
