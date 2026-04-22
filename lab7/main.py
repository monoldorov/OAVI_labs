from __future__ import annotations

from config import (
    ALPHABET,
    BASE_CASE_DIR,
    CANVAS_SIZE,
    FEATURE_COLUMNS,
    FONT_CANDIDATES,
    FONT_SIZE_BASE,
    FONT_SIZE_TEST,
    GROUND_TRUTH_SYMBOLS,
    HORIZONTAL_EMPTY_THRESHOLD,
    LETTER_SPACING,
    LINE_PADDING,
    MIN_SYMBOL_HEIGHT,
    MIN_SYMBOL_WIDTH,
    OUTPUT_DIR,
    PHRASE,
    REFERENCE_FEATURES_DIR,
    REFERENCE_SYMBOLS_DIR,
    REPORTS_DIR,
    SPACE_WIDTH,
    TEST_CASE_DIR,
    THRESHOLD,
    VERTICAL_EMPTY_THRESHOLD,
)
from font_utils import find_existing_font_path, load_font
from image_utils import (
    build_phrase_image_from_symbols,
    ensure_dirs,
    generate_reference_symbols,
    save_binary_png,
    save_boxes_visualization,
    save_crop,
)
from features import compute_symbol_features, save_reference_features_csv
from segmentation import segment_symbols_in_line
from classifier import (
    build_recognized_string,
    classify_symbol,
    evaluate_recognition,
    save_experiment_summary_csv,
    save_hypotheses_text,
    save_recognition_report,
)


def prepare_reference_database(font) -> dict[str, dict[str, float]]:
    reference_symbols = generate_reference_symbols(
        alphabet=ALPHABET,
        font=font,
        canvas_size=CANVAS_SIZE,
        threshold=THRESHOLD,
    )

    rows = []
    reference_db: dict[str, dict[str, float]] = {}

    for symbol, image in reference_symbols.items():
        save_binary_png(image, REFERENCE_SYMBOLS_DIR / f"{symbol}.png")

        features = compute_symbol_features(image)
        reference_db[symbol] = features

        row = {"symbol": symbol}
        row.update(features)
        rows.append(row)

    save_reference_features_csv(
        rows=rows,
        output_path=REFERENCE_FEATURES_DIR / "reference_features.csv",
    )

    return reference_db


def run_single_case(
    case_name: str,
    font_size: int,
    case_dir,
    reference_db: dict[str, dict[str, float]],
    font_path,
) -> dict[str, object]:
    case_dir.mkdir(parents=True, exist_ok=True)

    line_dir = case_dir / "line"
    crops_dir = case_dir / "crops"
    reports_dir = case_dir / "reports"

    ensure_dirs([line_dir, crops_dir, reports_dir])

    font = load_font(font_path, font_size)

    # Эталоны для сборки строки тем же способом, что в 5 и 6 лабах
    symbol_images = generate_reference_symbols(
        alphabet=ALPHABET,
        font=font,
        canvas_size=CANVAS_SIZE,
        threshold=THRESHOLD,
    )

    line_binary = build_phrase_image_from_symbols(
        phrase=PHRASE,
        symbol_images=symbol_images,
        letter_spacing=LETTER_SPACING,
        space_width=SPACE_WIDTH,
        line_padding=LINE_PADDING,
    )

    save_binary_png(line_binary, line_dir / "generated_text_line.png")

    boxes = segment_symbols_in_line(
        binary_black=line_binary,
        horizontal_empty_threshold=HORIZONTAL_EMPTY_THRESHOLD,
        vertical_empty_threshold=VERTICAL_EMPTY_THRESHOLD,
        min_symbol_width=MIN_SYMBOL_WIDTH,
        min_symbol_height=MIN_SYMBOL_HEIGHT,
    )

    save_boxes_visualization(
        binary_black=line_binary,
        boxes=boxes,
        output_path=line_dir / "text_line_boxes.png",
    )

    all_hypotheses = []

    for index, box in enumerate(boxes, start=1):
        save_crop(line_binary, box, crops_dir / f"{index:02d}.png")

        x1, y1, x2, y2 = box
        crop = line_binary[y1:y2 + 1, x1:x2 + 1]

        features = compute_symbol_features(crop)
        hypotheses = classify_symbol(
            unknown_features=features,
            reference_db=reference_db,
            feature_columns=FEATURE_COLUMNS,
        )
        all_hypotheses.append(hypotheses)

    recognized = build_recognized_string(all_hypotheses)
    metrics = evaluate_recognition(recognized, GROUND_TRUTH_SYMBOLS)

    save_hypotheses_text(
        all_hypotheses=all_hypotheses,
        output_path=reports_dir / "hypotheses.txt",
    )

    save_recognition_report(
        recognized=recognized,
        truth=GROUND_TRUTH_SYMBOLS,
        metrics=metrics,
        output_path=reports_dir / "recognition_report.txt",
    )

    return {
        "case_name": case_name,
        "font_size": font_size,
        "recognized": recognized,
        "truth": GROUND_TRUTH_SYMBOLS,
        "symbols_found": len(boxes),
        "correct": metrics["correct"],
        "errors": metrics["errors"],
        "accuracy_percent": round(float(metrics["accuracy_percent"]), 4),
    }


def main() -> None:
    ensure_dirs([
        OUTPUT_DIR,
        REFERENCE_SYMBOLS_DIR,
        REFERENCE_FEATURES_DIR,
        BASE_CASE_DIR,
        TEST_CASE_DIR,
        REPORTS_DIR,
    ])

    font_path = find_existing_font_path(FONT_CANDIDATES)
    reference_font = load_font(font_path, FONT_SIZE_BASE)

    # 1. База эталонов
    reference_db = prepare_reference_database(reference_font)

    # 2. Базовый случай
    base_result = run_single_case(
        case_name="base_case",
        font_size=FONT_SIZE_BASE,
        case_dir=BASE_CASE_DIR,
        reference_db=reference_db,
        font_path=font_path,
    )

    # 3. Эксперимент с другим размером шрифта
    test_result = run_single_case(
        case_name="changed_size_case",
        font_size=FONT_SIZE_TEST,
        case_dir=TEST_CASE_DIR,
        reference_db=reference_db,
        font_path=font_path,
    )

    # 4. Общий сводный файл
    save_experiment_summary_csv(
        rows=[base_result, test_result],
        output_path=REPORTS_DIR / "experiment_summary.csv",
    )

    print("Готово.")
    print(f"Шрифт: {font_path}")
    print(f"Эталоны символов: {REFERENCE_SYMBOLS_DIR}")
    print(f"Эталонные признаки: {REFERENCE_FEATURES_DIR / 'reference_features.csv'}")
    print(f"Базовый случай: {BASE_CASE_DIR}")
    print(f"Эксперимент с другим размером: {TEST_CASE_DIR}")
    print(f"Сводка: {REPORTS_DIR / 'experiment_summary.csv'}")


if __name__ == "__main__":
    main()