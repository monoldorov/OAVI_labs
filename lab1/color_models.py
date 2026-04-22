from os import path, makedirs
from PIL import Image
import numpy as np


BASE_DIR = path.dirname(path.abspath(__file__))
SRC_DIR = path.join(BASE_DIR, "pictures_src")
RESULTS_DIR = path.join(BASE_DIR, "pictures_results_1")


def image_to_np_array(image_name: str) -> np.ndarray:
    img_path = path.join(SRC_DIR, image_name)
    img_src = Image.open(img_path).convert("RGB")
    return np.array(img_src, dtype=np.uint8)


def save_rgb_image(arr: np.ndarray, filename: str):
    makedirs(RESULTS_DIR, exist_ok=True)
    save_path = path.join(RESULTS_DIR, filename)
    Image.fromarray(arr.astype(np.uint8), "RGB").save(save_path)


def save_gray_image(arr: np.ndarray, filename: str):
    makedirs(RESULTS_DIR, exist_ok=True)
    save_path = path.join(RESULTS_DIR, filename)
    Image.fromarray(arr.astype(np.uint8), "L").save(save_path)


def extract_rgb_channels(img: np.ndarray):
    r = np.zeros_like(img)
    g = np.zeros_like(img)
    b = np.zeros_like(img)

    r[:, :, 0] = img[:, :, 0]
    g[:, :, 1] = img[:, :, 1]
    b[:, :, 2] = img[:, :, 2]

    return r, g, b


def rgb_to_hsi(img: np.ndarray):
    rgb = img.astype(np.float64) / 255.0

    R = rgb[:, :, 0]
    G = rgb[:, :, 1]
    B = rgb[:, :, 2]

    eps = 1e-8

    I = (R + G + B) / 3.0

    min_rgb = np.minimum(np.minimum(R, G), B)
    sum_rgb = R + G + B
    S = np.zeros_like(I)
    mask = sum_rgb > eps
    S[mask] = 1.0 - 3.0 * min_rgb[mask] / sum_rgb[mask]
    S = np.clip(S, 0.0, 1.0)

    num = 0.5 * ((R - G) + (R - B))
    den = np.sqrt((R - G) ** 2 + (R - B) * (G - B)) + eps
    theta = np.arccos(np.clip(num / den, -1.0, 1.0))

    H = np.where(B <= G, theta, 2.0 * np.pi - theta)
    H = np.degrees(H)

    return H, S, I


def hsi_to_rgb(H: np.ndarray, S: np.ndarray, I: np.ndarray):
    H = np.mod(H, 360.0)

    R = np.zeros_like(I)
    G = np.zeros_like(I)
    B = np.zeros_like(I)

    mask1 = (H >= 0) & (H < 120)
    H1 = np.radians(H[mask1])
    B[mask1] = I[mask1] * (1 - S[mask1])
    R[mask1] = I[mask1] * (
        1 + (S[mask1] * np.cos(H1)) / (np.cos(np.radians(60) - H1) + 1e-8)
    )
    G[mask1] = 3 * I[mask1] - (R[mask1] + B[mask1])

    mask2 = (H >= 120) & (H < 240)
    H2 = np.radians(H[mask2] - 120)
    R[mask2] = I[mask2] * (1 - S[mask2])
    G[mask2] = I[mask2] * (
        1 + (S[mask2] * np.cos(H2)) / (np.cos(np.radians(60) - H2) + 1e-8)
    )
    B[mask2] = 3 * I[mask2] - (R[mask2] + G[mask2])

    mask3 = (H >= 240) & (H < 360)
    H3 = np.radians(H[mask3] - 240)
    G[mask3] = I[mask3] * (1 - S[mask3])
    B[mask3] = I[mask3] * (
        1 + (S[mask3] * np.cos(H3)) / (np.cos(np.radians(60) - H3) + 1e-8)
    )
    R[mask3] = 3 * I[mask3] - (G[mask3] + B[mask3])

    rgb = np.stack([R, G, B], axis=2)
    rgb = np.clip(rgb, 0.0, 1.0)
    return (rgb * 255).astype(np.uint8)


def process_color_models(image_name: str):
    img = image_to_np_array(image_name)

    r_img, g_img, b_img = extract_rgb_channels(img)
    save_rgb_image(r_img, "zhest_r.png")
    save_rgb_image(g_img, "zhest_g.png")
    save_rgb_image(b_img, "zhest_b.png")

    H, S, I = rgb_to_hsi(img)
    intensity_img = np.clip(I * 255.0, 0, 255).astype(np.uint8)
    save_gray_image(intensity_img, "zhest_intensity.png")

    I_inv = 1.0 - I
    inverted_img = hsi_to_rgb(H, S, I_inv)
    save_rgb_image(inverted_img, "zhest_hsi_inverted.png")


if __name__ == "__main__":
    process_color_models("zhest.png")
