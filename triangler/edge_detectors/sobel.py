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
    _, _, c = img.shape  # get the number of channels

    # Convert the image to grayscale if it has more than 1 channel
    if c > 1:
        img = np.dot(img[..., :3], [r_weight, g_weight, b_weight])

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
    grad_mag *= 255.0 / grad_mag.max()

    return grad_mag.astype(np.uint8)
