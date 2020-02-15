import numba
import numpy as np
from numpy.random import choice


@numba.jit
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

    return candidates[choice(candidates.shape[0], size=n, replace=False)]
