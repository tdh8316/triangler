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
    if img.ndim == 3:
        if img.shape[2] > 1:  # RGB/RGBA
            img = np.dot(img[..., :3], [r_weight, g_weight, b_weight])
        else:
            img = img[..., 0]
    elif img.ndim != 2:
        raise ValueError(
            "Invalid image shape. Expected 2D (grayscale) or 3D (color) array "
            + f"but got shape={img.shape}."
        )

    # Canny edge detection
    edges: np.ndarray = feature.canny(
        img,
        sigma=config.sigma,
        low_threshold=config.low_threshold,
        high_threshold=config.high_threshold,
    )

    return edges
