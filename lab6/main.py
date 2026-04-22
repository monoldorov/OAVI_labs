from __future__ import annotations

from config import (
    ALPHABET,
    ALPHABET_PROFILES_DIR,
    BOXES_DIR,
    CANVAS_SIZE,
    CROPS_DIR,
    FONT_CANDIDATES,
    FONT_SIZE,
    GENERATED_DIR,
    HORIZONTAL_EMPTY_THRESHOLD,
    INPUT_LINE_PATH,
    INPUT_MODE,
    LETTER_SPACING,
    LINE_PADDING,
    MIN_SYMBOL_HEIGHT,
    MIN_SYMBOL_WIDTH,
    OUTPUT_DIR,
    PHRASE,
    PROFILES_DIR,
    SPACE_WIDTH,
    THRESHOLD,
    VERTICAL_EMPTY_THRESHOLD,
)
from font_utils import find_existing_font_path, load_font
from image_utils import (
    build_phrase_image_from_symbols,
    crop_white_margins,
    ensure_dirs,
    load_bmp_as_binary_black,
    render_symbol_to_binary,
    save_binary_bmp,
    save_binary_png,
    save_boxes_visualization,
    save_crop,
)
from profiles import (
    horizontal_profile,
    save_profile_plot,
    vertical_profile,
)
from segmentation import segment_symbols_in_line


def generate_symbol_images(font) -> dict[str, object]:

    result = {}
    for symbol in ALPHABET:
        binary = render_symbol_to_binary(
            symbol=symbol,
            font=font,
            canvas_size=CANVAS_SIZE,
            threshold=THRESHOLD,
        )
        cropped = crop_white_margins(binary)
        result[symbol] = cropped
    return result


def save_generated_symbols(symbol_images: dict[str, object]) -> None:
    symbols_dir = GENERATED_DIR / "symbols"
    ensure_dirs([symbols_dir])

    for symbol, image in symbol_images.items():
        save_binary_png(image, symbols_dir / f"{symbol}.png")


def generate_alphabet_profiles(symbol_images: dict[str, object]) -> None:

    for symbol, image in symbol_images.items():
        h_profile = horizontal_profile(image)
        v_profile = vertical_profile(image)

        save_profile_plot(
            values=h_profile,
            coordinate_name="y",
            output_path=ALPHABET_PROFILES_DIR / f"{symbol}_horizontal_profile.png",
            title=f"Horizontal profile for '{symbol}'",
        )

        save_profile_plot(
            values=v_profile,
            coordinate_name="x",
            output_path=ALPHABET_PROFILES_DIR / f"{symbol}_vertical_profile.png",
            title=f"Vertical profile for '{symbol}'",
        )


def get_input_line_binary(symbol_images: dict[str, object]):

    if INPUT_MODE == "bmp":
        if not INPUT_LINE_PATH.exists():
            raise FileNotFoundError(
                f"Не найден входной файл: {INPUT_LINE_PATH}\n"
                "Подготовь input/text_line.bmp или переключи INPUT_MODE='generated'."
            )
        return load_bmp_as_binary_black(INPUT_LINE_PATH, THRESHOLD)

    if INPUT_MODE == "generated":
        line_binary = build_phrase_image_from_symbols(
            phrase=PHRASE,
            symbol_images=symbol_images,
            letter_spacing=LETTER_SPACING,
            space_width=SPACE_WIDTH,
            line_padding=LINE_PADDING,
        )

        save_binary_png(line_binary, GENERATED_DIR / "generated_text_line.png")
        save_binary_bmp(line_binary, GENERATED_DIR / "generated_text_line.bmp")
        return line_binary

    raise ValueError(f"Неизвестный INPUT_MODE: {INPUT_MODE}")


def main() -> None:
    ensure_dirs(
        [
            OUTPUT_DIR,
            GENERATED_DIR,
            PROFILES_DIR,
            BOXES_DIR,
            CROPS_DIR,
            ALPHABET_PROFILES_DIR,
        ]
    )

    font_path = find_existing_font_path(FONT_CANDIDATES)
    font = load_font(font_path, FONT_SIZE)

    symbol_images = generate_symbol_images(font)
    save_generated_symbols(symbol_images)

    generate_alphabet_profiles(symbol_images)

    line_binary = get_input_line_binary(symbol_images)

    h_profile = horizontal_profile(line_binary)
    v_profile = vertical_profile(line_binary)

    save_profile_plot(
        values=h_profile,
        coordinate_name="y",
        output_path=PROFILES_DIR / "text_line_horizontal_profile.png",
        title="Horizontal profile of text line",
    )

    save_profile_plot(
        values=v_profile,
        coordinate_name="x",
        output_path=PROFILES_DIR / "text_line_vertical_profile.png",
        title="Vertical profile of text line",
    )

    boxes = segment_symbols_in_line(
        binary_black=line_binary,
        horizontal_empty_threshold=HORIZONTAL_EMPTY_THRESHOLD,
        vertical_empty_threshold=VERTICAL_EMPTY_THRESHOLD,
        min_symbol_width=MIN_SYMBOL_WIDTH,
        min_symbol_height=MIN_SYMBOL_HEIGHT,
    )

    if not boxes:
        raise ValueError("Не удалось сегментировать строку на символы.")

    save_boxes_visualization(
        binary_black=line_binary,
        boxes=boxes,
        output_path=BOXES_DIR / "text_line_boxes.png",
    )

    for index, box in enumerate(boxes, start=1):
        save_crop(
            binary_black=line_binary,
            box=box,
            output_path=CROPS_DIR / f"{index:02d}.png",
        )

    print("Готово.")
    print(f"Режим ввода: {INPUT_MODE}")
    print(f"Фраза: {PHRASE}")
    print(f"Шрифт: {font_path}")
    print(f"Сгенерированные символы: {GENERATED_DIR / 'symbols'}")
    if INPUT_MODE == "generated":
        print(
            f"Сгенерированная строка PNG: {GENERATED_DIR / 'generated_text_line.png'}"
        )
        print(
            f"Сгенерированная строка BMP: {GENERATED_DIR / 'generated_text_line.bmp'}"
        )
    else:
        print(f"Входная строка BMP: {INPUT_LINE_PATH}")
    print(f"Профили строки: {PROFILES_DIR}")
    print(f"Строка с рамками: {BOXES_DIR}")
    print(f"Вырезанные символы: {CROPS_DIR}")
    print(f"Профили алфавита: {ALPHABET_PROFILES_DIR}")
    print(f"Найдено символов: {len(boxes)}")


if __name__ == "__main__":
    main()
