import warnings as _warnings
from typing import Union

import numba
import numpy as np
from numpy.core.multiarray import ndarray
from scipy.spatial import Delaunay
from skimage.draw import polygon
from skimage.io import imread
from skimage.transform import pyramid_reduce

from triangler.color import ColorMethod
from triangler.edges import EdgePoints, EdgeMethod
from triangler.sampling import SampleMethod

np.random.seed(822)
_warnings.filterwarnings("ignore")


@numba.jit(fastmath=True, parallel=True)
def process(
    img: Union[ndarray, str],
    coloring: ColorMethod,
    sampling: SampleMethod,
    edging: EdgeMethod,
    points: int,
    blur: int,
    reduce: bool,
) -> np.array:
    if isinstance(img, str):
        img = imread(img)
    sample_points: ndarray = EdgePoints(img, points, edging).get_edge_points(
        sampling=sampling, blur=blur,
    )
    triangulated: Delaunay = Delaunay(sample_points)

    # noinspection PyUnresolvedReferences
    triangles = sample_points[triangulated.simplices]

    res = np.empty(
        shape=(2 * img.shape[0], 2 * img.shape[1], img.shape[2]), dtype=np.uint8
    )

    if coloring is ColorMethod.CENTROID:
        for triangle in triangles:
            i, j = polygon(2 * triangle[:, 0], 2 * triangle[:, 1], res.shape)
            res[i, j] = img[tuple(np.mean(triangle, axis=0, dtype=np.int32))]
    elif coloring is ColorMethod.MEAN:
        for triangle in triangles:
            i, j = polygon(2 * triangle[:, 0], 2 * triangle[:, 1], res.shape)
            res[i, j] = np.mean(
                img[polygon(triangle[:, 0], triangle[:, 1], img.shape)], axis=0
            )
    else:
        raise ValueError(
            "Unexpected coloring method: {}\n"
            "use {} instead: {}".format(
                coloring, ColorMethod.__name__, ColorMethod.__members__
            )
        )

    return pyramid_reduce(res, multichannel=True) if reduce else res
