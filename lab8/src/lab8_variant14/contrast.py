import numpy as np


def logarithmic_contrast_transform(gray: np.ndarray) -> np.ndarray:

    gray = gray.astype(np.float32)

    mean = float(np.mean(gray))
    fmin = float(np.min(gray))
    fmax = float(np.max(gray))

    positive_denom = max(2.0, fmax - mean)
    negative_denom = max(2.0, mean - fmin)

    positive_alpha = 255.0 / np.log1p(positive_denom)
    negative_alpha = 255.0 / np.log1p(negative_denom)

    diff = gray - mean
    result = np.empty_like(gray)

    positive_mask = diff >= 0
    negative_mask = ~positive_mask

    result[positive_mask] = mean + positive_alpha * np.log1p(diff[positive_mask])
    result[negative_mask] = mean - negative_alpha * np.log1p(-diff[negative_mask])

    return np.clip(result, 0, 255)
