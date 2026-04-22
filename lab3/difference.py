import cv2
import numpy as np


def xor_difference(original, processed):

    return cv2.bitwise_xor(original, processed)


def abs_difference(original, processed):

    return cv2.absdiff(original, processed)


def enhance_difference(diff, factor=10):

    enhanced = diff.astype(np.float32) * factor
    enhanced = np.clip(enhanced, 0, 255)
    return enhanced.astype(np.uint8)
