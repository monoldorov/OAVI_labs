from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = PROJECT_ROOT / "input" / "images"
OUTPUT_DIR = PROJECT_ROOT / "output"

GRAY_DIR = OUTPUT_DIR / "gray"
CONTRAST_GRAY_DIR = OUTPUT_DIR / "contrast_gray"
COLOR_CONTRAST_DIR = OUTPUT_DIR / "color_contrast"
HIST_BEFORE_DIR = OUTPUT_DIR / "hist_before"
HIST_AFTER_DIR = OUTPUT_DIR / "hist_after"
MATRIX_BEFORE_DIR = OUTPUT_DIR / "matrix_before"
MATRIX_AFTER_DIR = OUTPUT_DIR / "matrix_after"
TABLES_DIR = OUTPUT_DIR / "tables"

ALL_OUTPUT_DIRS = [
    OUTPUT_DIR,
    GRAY_DIR,
    CONTRAST_GRAY_DIR,
    COLOR_CONTRAST_DIR,
    HIST_BEFORE_DIR,
    HIST_AFTER_DIR,
    MATRIX_BEFORE_DIR,
    MATRIX_AFTER_DIR,
    TABLES_DIR,
]

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

GLRLM_LEVELS = 16

GLRLM_DIRECTIONS = [
    (0, 1),  # 0°
    (-1, 1),  # 45°
    (1, 0),  # 90°
    (1, -1),  # 135°
]

HIST_BINS = 256
