from dataclasses import dataclass

import numpy as np
from skimage import feature


@dataclass
class CannyConfig:
    r_weight: float = 0.2126
    g_weight: float = 0.7152
    b_weight: float = 0.0722
    sigma: float = 3.0
    low_threshold: float = 0.1
    high_threshold: float = 0.2


def canny(
    img: np.ndarray,
    config: CannyConfig,
) -> np.ndarray:
    # Convert the image to grayscale
    r_weight, g_weight, b_weight = config.r_weight, config.g_weight, config.b_weight
    if img.shape[-1] > 1:  # if the image is multichannel
        img = np.dot(img[..., :3], [r_weight, g_weight, b_weight])

    # Canny edge detection
    edges: np.ndarray = feature.canny(
        img,
        sigma=config.sigma,
        low_threshold=config.low_threshold,
        high_threshold=config.high_threshold,
    )

    return edges
