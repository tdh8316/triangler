from dataclasses import dataclass

import numpy as np
import scipy


@dataclass
class PoissonDiskConfig:
    n_iter: int = 16
    eps: float = 1e-6


def poisson_disk_sampling(
    weights: np.ndarray,
    n_samples: int,
    config: PoissonDiskConfig = PoissonDiskConfig(),
) -> np.ndarray:
    n_iter: int = config.n_iter

    w: int = weights.shape[0]
    h: int = weights.shape[1]

    rad_max = int(min(w, h) / 4)
    _factor = 1 / np.log10(w * h) / 2
    rad_avg = np.sqrt((w * h) / (_factor * np.pi * n_samples))

    # Normalize the weights
    weights = weights / weights.mean()

    rads = np.clip(
        rad_avg / (weights + config.eps),
        a_min=rad_avg / 4,
        a_max=rad_max,
    )

    first: tuple = (
        np.random.randint(w),
        np.random.randint(h),
    )
    queue: list = [first]
    sample_points: list = [first]

    tree = scipy.spatial.cKDTree(sample_points)

    def _get_point_near(_point: tuple):
        r = np.random.uniform(rads[_point], rad_max)
        theta = np.random.uniform(0, 2 * np.pi)
        _new_point = (
            _point[0] + r * np.cos(theta),
            _point[1] + r * np.sin(theta),
        )
        return (
            int(_new_point[0]),
            int(_new_point[1]),
        )

    def _in_bounds(_point: tuple) -> bool:
        return 0 <= _point[0] < w and 0 <= _point[1] < h

    def _has_neighbors(_new_point: tuple, _tree: scipy.spatial.cKDTree) -> bool:
        balls = _tree.query_ball_point(_new_point, rads[_new_point])  # type: ignore
        return len(balls) > 0

    while queue and len(sample_points) < n_samples:
        idx = np.random.randint(len(queue))
        point = queue[idx]

        success = False
        for _ in range(n_iter):
            new_point = _get_point_near(point)
            if _in_bounds(new_point) and not _has_neighbors(new_point, tree):
                queue.append(new_point)
                sample_points.append(new_point)
                tree = scipy.spatial.cKDTree(sample_points)
                success = True
                break

        if not success:
            queue.pop(idx)

    return np.array(sample_points)
