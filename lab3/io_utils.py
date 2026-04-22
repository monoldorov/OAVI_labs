from pathlib import Path
import cv2

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def ensure_directories(directories: list[Path]) -> None:
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def list_images(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in VALID_EXTENSIONS])


def read_grayscale_image(path: Path):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {path}")
    return img


def build_output_name(input_path: Path, algorithm_suffix: str) -> str:

    stem = input_path.stem
    return f"{stem}.{algorithm_suffix}.png"


def save_image(
    output_dir: Path, input_path: Path, image, algorithm_suffix: str
) -> Path:

    output_path = output_dir / build_output_name(input_path, algorithm_suffix)
    ok = cv2.imwrite(str(output_path), image)
    if not ok:
        raise ValueError(f"Не удалось сохранить изображение: {output_path}")
    return output_path
