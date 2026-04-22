from pathlib import Path

# Вариант 14
ALPHABET = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

# Исходная строка
PHRASE = "TE QUIERO"

# Для посимвольной проверки без пробела
GROUND_TRUTH_SYMBOLS = "TEQUIERO"

# Бакалавр: только признаки, без Левенштейна по профилям
IS_MASTER = False

# Базовый и экспериментальный размеры шрифта
FONT_SIZE_BASE = 180
FONT_SIZE_TEST = 188

CANVAS_SIZE = (260, 260)
THRESHOLD = 200

# Сборка строки
LETTER_SPACING = 10
SPACE_WIDTH = 35
LINE_PADDING = 4

# Сегментация
HORIZONTAL_EMPTY_THRESHOLD = 1
VERTICAL_EMPTY_THRESHOLD = 1
MIN_SYMBOL_WIDTH = 2
MIN_SYMBOL_HEIGHT = 2

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

REFERENCE_SYMBOLS_DIR = OUTPUT_DIR / "reference_symbols"
REFERENCE_FEATURES_DIR = OUTPUT_DIR / "reference_features"

BASE_CASE_DIR = OUTPUT_DIR / "base_case"
TEST_CASE_DIR = OUTPUT_DIR / "changed_size_case"

REPORTS_DIR = OUTPUT_DIR / "reports"

# Системные шрифты
FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\times.ttf"),
    Path(r"C:\Windows\Fonts\timesbd.ttf"),
    Path(r"C:\Windows\Fonts\arial.ttf"),
    Path(r"C:\Windows\Fonts\calibri.ttf"),
    Path("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"),
    Path("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"),
    Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
]

# Признаки для классификации по условию:
# масса, координаты центра тяжести, осевые моменты инерции
FEATURE_COLUMNS = [
    "weight_rel",
    "center_x_rel",
    "center_y_rel",
    "ix_rel",
    "iy_rel",
]