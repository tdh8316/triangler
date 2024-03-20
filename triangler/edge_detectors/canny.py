from dataclasses import dataclass

import numpy as np


@dataclass
class CannyConfig:
    pass


def canny(
    img: np.ndarray,
    config: CannyConfig = CannyConfig(),
) -> np.ndarray:
    raise NotImplementedError("Canny edge detection is not implemented yet.")
