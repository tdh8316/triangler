from dataclasses import dataclass

import numpy as np


@dataclass
class EntropyConfig:
    pass


def entropy(
    img: np.ndarray,
    config: EntropyConfig = EntropyConfig(),
) -> np.ndarray:
    raise NotImplementedError("Entropy edge detection is not implemented yet.")
