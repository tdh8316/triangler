from typing import Tuple

import numba
import numpy as np
from numpy import random
from scipy.spatial import KDTree


@numba.jit
def poisson_disk_sample(n, weights):
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
    ist :
        List of sampled points
    """
    width = weights.shape[0]
    height = weights.shape[1]

    c = np.log10(width * height) / 2
    max_rad = min(width, height) / 4
    avg_rad = np.sqrt((height * width) / ((1 / c) * n * np.pi))
    min_rad = avg_rad / 4

    weights = weights / np.mean(weights)
    rads = np.clip(avg_rad / (weights + 0.01), min_rad, max_rad)

    first = (random.randint(width), random.randint(height))
    queue = [first]
    sample_points = [first]
    tree = KDTree(sample_points)

    while queue and len(sample_points) < n:
        idx = random.randint(len(queue))
        point = queue[idx]

        success = False
        for it in range(16):
            new_point = get_point_near(point, rads, max_rad)

            if (0 <= new_point[0] < width and 0 <= new_point[1] < height) and (
                len(tree.query_ball_point(new_point, rads[new_point])) > 0
            ):
                queue.append(new_point)
                sample_points.append(new_point)
                tree = KDTree(sample_points)
                success = True
                break

        if not success:
            queue.pop(idx)

    return np.array(list(sample_points))


@numba.jit
def get_point_near(point, rads, max_rad) -> Tuple[int, int]:
    """
    Randomly samples an annulus near a given point using a uniform
    distribution.
    Parameters
    ----------
    point : (int, int)
        The point to sample nearby.
    rads : np.array
        The lower bound for the random search.
    max_rad : int
        The upper bound for the random search.

    Returns
    -------
    (int, int) :
        The nearby point.
    """
    rad = random.uniform(rads[point], max_rad)
    theta = random.uniform(0, 2 * np.pi)
    new_point = (point[0] + rad * np.cos(theta), point[1] + rad * np.sin(theta))
    return int(new_point[0]), int(new_point[1])
