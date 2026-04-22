import csv

from config import (
    ALPHABET,
    CANVAS_SIZE,
    CSV_PATH,
    FONT_CANDIDATES,
    FONT_SIZE,
    OUTPUT_DIR,
    PROFILES_X_DIR,
    PROFILES_Y_DIR,
    PROFILE_X_SUFFIX,
    PROFILE_Y_SUFFIX,
    SYMBOLS_DIR,
    THRESHOLD,
)
from font_utils import find_existing_font_path, load_font
from image_features import (
    compute_profiles,
    compute_scalar_features,
    crop_white_margins,
    csv_columns,
    format_csv_value,
    make_safe_stem,
    render_symbol_to_binary,
    save_binary_png,
    save_profile_plot,
)


def ensure_output_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SYMBOLS_DIR.mkdir(parents=True, exist_ok=True)
    PROFILES_X_DIR.mkdir(parents=True, exist_ok=True)
    PROFILES_Y_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(rows: list[dict]) -> None:
    columns = csv_columns()

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(columns)

        for row in rows:
            writer.writerow([format_csv_value(row[column]) for column in columns])


def main() -> None:
    ensure_output_dirs()

    font_path = find_existing_font_path(FONT_CANDIDATES)
    font = load_font(font_path, FONT_SIZE)

    rows: list[dict] = []

    for symbol in ALPHABET:
        stem = make_safe_stem(symbol)

        binary = render_symbol_to_binary(
            symbol=symbol,
            font=font,
            canvas_size=CANVAS_SIZE,
            threshold=THRESHOLD,
        )

        cropped = crop_white_margins(binary)

        symbol_file_name = f"{stem}.png"
        symbol_path = SYMBOLS_DIR / symbol_file_name
        save_binary_png(cropped, symbol_path)

        features = compute_scalar_features(
            symbol=symbol,
            image_file=symbol_file_name,
            binary_black=cropped,
        )
        rows.append(features)

        profile_x, profile_y = compute_profiles(cropped)

        save_profile_plot(
            values=profile_x,
            coordinate_name="x",
            output_path=PROFILES_X_DIR / f"{stem}{PROFILE_X_SUFFIX}",
            title=f"Profile X for '{symbol}'",
        )

        save_profile_plot(
            values=profile_y,
            coordinate_name="y",
            output_path=PROFILES_Y_DIR / f"{stem}{PROFILE_Y_SUFFIX}",
            title=f"Profile Y for '{symbol}'",
        )

    write_csv(rows)

    print("Готово.")
    print(f"Шрифт: {font_path}")
    print(f"Символы: {SYMBOLS_DIR}")
    print(f"Профили X: {PROFILES_X_DIR}")
    print(f"Профили Y: {PROFILES_Y_DIR}")
    print(f"CSV: {CSV_PATH}")


if __name__ == "__main__":
    main()
