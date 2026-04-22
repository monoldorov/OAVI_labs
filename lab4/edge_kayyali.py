import cv2
import numpy as np


KAYYALI_GX = np.array([[6, 0, -6], [0, 0, 0], [-6, 0, 6]], dtype=np.float32)

KAYYALI_GY = np.array([[-6, 0, 6], [0, 0, 0], [6, 0, -6]], dtype=np.float32)


def apply_kayyali(gray_image: np.ndarray):
    gray_float = gray_image.astype(np.float32)

    gx = cv2.filter2D(gray_float, ddepth=cv2.CV_32F, kernel=KAYYALI_GX)
    gy = cv2.filter2D(gray_float, ddepth=cv2.CV_32F, kernel=KAYYALI_GY)

    gradient = np.abs(gx) + np.abs(gy)

    return gx, gy, gradient
