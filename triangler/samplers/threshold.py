from dataclasses import dataclass

import numpy as np


@dataclass
class ThresholdConfig:
    pass


def threshold_sampling(
    img: np.ndarray,
    n_samples: int,
    config: ThresholdConfig = ThresholdConfig(),
) -> np.ndarray:
    raise NotImplementedError("Threshold sampling is not implemented yet.")
