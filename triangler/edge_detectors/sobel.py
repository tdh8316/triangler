from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.signal import convolve2d


@dataclass
class SobelConfig:
    r_weight: float = 0.2126
    g_weight: float = 0.7152
    b_weight: float = 0.0722
    kernel_x: Optional[np.ndarray] = None
    kernel_y: Optional[np.ndarray] = None


def sobel(
    img: np.ndarray,
    config: SobelConfig,
) -> np.ndarray:
    r_weight, g_weight, b_weight = config.r_weight, config.g_weight, config.b_weight
    kernel_x, kernel_y = config.kernel_x, config.kernel_y

    img = img.astype(np.float32)
    if img.ndim == 3:
        # Convert RGB/RGBA to grayscale using luminance weights.
        if img.shape[2] > 1:
            img = np.dot(img[..., :3], [r_weight, g_weight, b_weight])
        else:
            img = img[..., 0]
    elif img.ndim != 2:
        raise ValueError(
            "Invalid image shape. Expected 2D (grayscale) or 3D (color) array "
            + f"but got shape={img.shape}."
        )

    # Sobel kernels
    if kernel_x is None:
        kernel_x = np.array(
            [
                [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1],
            ],
            dtype=np.float32,
        )
    if kernel_y is None:
        kernel_y = np.array(
            [
                [-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1],
            ],
            dtype=np.float32,
        )

    # Convolve the image with the kernels
    img_x = convolve2d(img, kernel_x, mode="same", boundary="symm")
    img_y = convolve2d(img, kernel_y, mode="same", boundary="symm")

    # Calculate the gradient magnitude
    grad_mag = np.sqrt(img_x**2 + img_y**2)

    # Normalize the gradient magnitude
    max_grad = grad_mag.max()
    if max_grad > 0:
        grad_mag *= 255.0 / max_grad
    else:
        grad_mag.fill(0)

    return grad_mag.astype(np.uint8)
