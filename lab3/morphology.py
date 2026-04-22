import cv2
import numpy as np

# Вариант 14: квадрат 3x3
KERNEL_3X3 = np.ones((3, 3), dtype=np.uint8)


def binarize_image(gray_img):

    _, binary = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    return binary


def dilate_black_object(binary_img):

    inverted = cv2.bitwise_not(binary_img)
    dilated = cv2.dilate(inverted, KERNEL_3X3, iterations=1)
    result = cv2.bitwise_not(dilated)
    return result


def dilate_semitone(gray_img):
    return cv2.dilate(gray_img, KERNEL_3X3, iterations=1)
