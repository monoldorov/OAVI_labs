from typing import Tuple

import numpy as np
from PIL import Image
import colorsys


def rgb_image_to_hsl_arrays(
    image: Image.Image,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    rgb = np.asarray(image).astype(np.float32) / 255.0
    h = np.zeros((rgb.shape[0], rgb.shape[1]), dtype=np.float32)
    s = np.zeros_like(h)
    l = np.zeros_like(h)

    for y in range(rgb.shape[0]):
        for x in range(rgb.shape[1]):
            r, g, b = rgb[y, x]
            hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
            h[y, x] = hh
            s[y, x] = ss
            l[y, x] = ll

    return h, s, l


def hsl_arrays_to_rgb_image(h: np.ndarray, s: np.ndarray, l: np.ndarray) -> Image.Image:

    rgb = np.zeros((h.shape[0], h.shape[1], 3), dtype=np.float32)

    for y in range(h.shape[0]):
        for x in range(h.shape[1]):
            r, g, b = colorsys.hls_to_rgb(
                float(h[y, x]), float(l[y, x]), float(s[y, x])
            )
            rgb[y, x] = [r, g, b]

    rgb_uint8 = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(rgb_uint8, mode="RGB")


def lightness_to_uint8_image(lightness: np.ndarray) -> Image.Image:
    arr = np.clip(lightness * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="L")
