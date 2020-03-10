"""
Based on: https://github.com/pmaldonado/PyTri/blob/master/delaunay.py#L56
"""

import enum
from typing import Tuple

import numba
import numpy as np
import scipy.spatial


class SampleMethod(enum.Enum):
    __dict__ = ("POISSON_DISK", "THRESHOLD")

    POISSON_DISK = enum.auto()
    THRESHOLD = enum.auto()


@numba.jit(nopython=True, parallel=True)
def in_bounds(point: Tuple[int, int], width: int, height: int) -> bool:
    return 0 <= point[0] < width and 0 <= point[1] < height


@numba.jit
def has_neighbor(
    new_point: Tuple[int, int], rads: np.ndarray, tree: scipy.spatial.KDTree
) -> bool:
    return len(tree.query_ball_point(new_point, rads[new_point])) > 0


@numba.jit(fastmath=True, parallel=True)
def poisson_disk_sample(n: int, weights: np.array) -> np.ndarray:
    """
    Performs weighted poisson disk sampling over a region.
    Algorithm based on
    https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf
    Weighted approach inspired by
    https://codegolf.stackexchange.com/questions/50299/draw-an-image-as-a-voronoi-map
    Parameters
    ----------
    n : int
        The number of points to sample.
    weights : np.array
        Weights of grid to sample over. Assumes weights are normalized.

    Returns
    -------
    list :
        List of sampled points
    """
    width: int = weights.shape[0]
    height: int = weights.shape[1]

    max_rad: int = int(min(width, height) / 4)
    avg_rad = np.sqrt(
        (height * width) / ((1 / np.log10(width * height) / 2) * n * np.pi)
    )

    weights /= np.mean(weights)
    rads = np.clip(avg_rad / (weights + 0.01), avg_rad / 4, max_rad)

    first = (np.random.randint(width), np.random.randint(height))
    queue = [first]
    sample_points = [first]
    tree = scipy.spatial.KDTree(sample_points)

    while queue and len(sample_points) < n:
        idx = np.random.randint(len(queue))
        point = queue[idx]

        success = False
        for _ in numba.prange(16):
            new_point = get_point_near(point, rads, max_rad)

            if in_bounds(new_point, width=width, height=height) and not has_neighbor(
                new_point, rads, tree
            ):
                queue.append(new_point)
                sample_points.append(new_point)
                tree = scipy.spatial.KDTree(sample_points)
                success = True
                break

        if not success:
            queue.pop(idx)

    return np.array(list(sample_points))


@numba.jit(parallel=True, nopython=True)
def get_point_near(
    point: Tuple[int, int], rads: np.array, max_rad: int
) -> Tuple[int, int]:
    """
    Randomly samples an annulus near a given point using a uniform
    distribution.
    Parameters
    ----------
    point : (int, int)
        The point to sample nearby.
    rads : np.array
        The lower bound for the np.random search.
    max_rad : int
        The upper bound for the np.random search.

    Returns
    -------
    (int, int) :
        The nearby point.
    """
    rad = np.random.uniform(rads[point], max_rad)
    theta = np.random.uniform(0, 2 * np.pi)
    new_point = (point[0] + rad * np.cos(theta), point[1] + rad * np.sin(theta))
    return int(new_point[0]), int(new_point[1])


@numba.jit(parallel=True, nopython=True)
def threshold_sample(n, weights, threshold):
    """
    Sample the weighted points uniformly above a certain threshold.
    Parameters
    ----------
    n : int
        The number of points to sample.
    weights : np.array
        Weights of grid to sample over. Assumes weights are normalized.
    threshold : float
        The threshold to ignore points
    Returns
    -------
    list :
        The list of points to triangulate.
    """
    candidates = np.array(
        [idx for idx, weight in np.ndenumerate(weights) if weight >= threshold]
    )
    if candidates.shape[0] < n:
        n = candidates.shape[0]

    return candidates[np.random.choice(candidates.shape[0], size=n, replace=False)]
