from pathlib import Path
import cv2


BASE_DIR = Path(__file__).resolve().parent

INPUT_COLOR_DIR = BASE_DIR / "input" / "pictures_color_src"
INPUT_SEMITONE_DIR = BASE_DIR / "input" / "pictures_semitone_src"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_PATHS = {
    "color": {
        "gray": OUTPUT_DIR / "results_color_gray",
        "gx": OUTPUT_DIR / "results_color_gx",
        "gy": OUTPUT_DIR / "results_color_gy",
        "gradient": OUTPUT_DIR / "results_color_gradient",
        "binary": OUTPUT_DIR / "results_color_binary",
    },
    "semitone": {
        "gray": OUTPUT_DIR / "results_semitone_gray",
        "gx": OUTPUT_DIR / "results_semitone_gx",
        "gy": OUTPUT_DIR / "results_semitone_gy",
        "gradient": OUTPUT_DIR / "results_semitone_gradient",
        "binary": OUTPUT_DIR / "results_semitone_binary",
    },
}


def ensure_directories() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    for group in OUTPUT_PATHS.values():
        for folder in group.values():
            folder.mkdir(parents=True, exist_ok=True)


def get_image_files(folder: Path):
    if not folder.exists():
        print(f"[WARNING] Folder not found: {folder}")
        return []

    allowed_ext = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
    files = sorted([p for p in folder.iterdir() if p.suffix.lower() in allowed_ext])

    print(f"[INFO] Found {len(files)} files in: {folder}")
    return files


def read_color_image(path: Path):
    return cv2.imread(str(path), cv2.IMREAD_COLOR)


def read_grayscale_image(path: Path):
    return cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)


def save_image(path: Path, image) -> None:
    ok = cv2.imwrite(str(path), image)
    if not ok:
        print(f"[ERROR] Failed to save image: {path}")


def make_output_name(stem: str, suffix: str, threshold: int | None = None) -> str:
    if threshold is None:
        return f"{stem}_kayyali_{suffix}.png"
    return f"{stem}_kayyali_{suffix}_t{threshold}.png"
