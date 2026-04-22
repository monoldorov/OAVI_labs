from pathlib import Path

ALPHABET = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
PHRASE = "TE QUIERO"

INPUT_MODE = "generated"

CANVAS_SIZE = (260, 260)
FONT_SIZE = 180
THRESHOLD = 200

LETTER_SPACING = 10  
SPACE_WIDTH = 35 
LINE_PADDING = 4  

HORIZONTAL_EMPTY_THRESHOLD = 1
VERTICAL_EMPTY_THRESHOLD = 1
MIN_SYMBOL_WIDTH = 2
MIN_SYMBOL_HEIGHT = 2

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_LINE_PATH = INPUT_DIR / "text_line.bmp"

GENERATED_DIR = OUTPUT_DIR / "generated"
PROFILES_DIR = OUTPUT_DIR / "profiles"
BOXES_DIR = OUTPUT_DIR / "boxes"
CROPS_DIR = OUTPUT_DIR / "crops"
ALPHABET_PROFILES_DIR = OUTPUT_DIR / "alphabet_profiles"

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
