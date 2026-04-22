from pathlib import Path

ALPHABET = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

CANVAS_SIZE = (260, 260)
FONT_SIZE = 180
THRESHOLD = 200

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
SYMBOLS_DIR = OUTPUT_DIR / "symbols"
PROFILES_X_DIR = OUTPUT_DIR / "profiles_x"
PROFILES_Y_DIR = OUTPUT_DIR / "profiles_y"
CSV_PATH = OUTPUT_DIR / "scalar_features.csv"


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


PROFILE_X_SUFFIX = "_profile_x.png"
PROFILE_Y_SUFFIX = "_profile_y.png"
