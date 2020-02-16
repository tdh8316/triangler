import warnings

import numba
import numpy as np
from imageio import imread
from numba.errors import NumbaWarning
from numpy.core.multiarray import ndarray
from scipy.spatial import Delaunay
from skimage.draw import polygon
from skimage.transform import pyramid_reduce

from triangler.color import ColorMethod
from triangler.edges import Point, EdgeMethod
from triangler.sampling import SampleMethod

warnings.simplefilter("ignore", category=NumbaWarning)


@numba.jit(fastmath=True, parallel=True)
def main(
    path: str,
    coloring: ColorMethod,
    sampling: SampleMethod,
    edging: EdgeMethod,
    points: int,
    blur: int = 2,
):
    img: ndarray = imread(path)
    sample_points: ndarray = Point(img, points, edging).generate(blur, sampling)
    triangulated: Delaunay = Delaunay(sample_points)

    # noinspection PyUnresolvedReferences
    triangles = sample_points[triangulated.simplices]

    res = np.empty(
        shape=(2 * img.shape[0], 2 * img.shape[1], img.shape[2]), dtype=np.uint8
    )

    for triangle in triangles:
        i, j = polygon(2 * triangle[:, 0], 2 * triangle[:, 1], res.shape)

        if coloring is ColorMethod.CENTROID:
            color = img[tuple(np.mean(triangle, axis=0, dtype=np.int32))]
        elif coloring is ColorMethod.MEAN:
            color = np.mean(
                img[polygon(triangle[:, 0], triangle[:, 1], img.shape)], axis=0
            )
        else:
            raise ValueError(
                "Unexpected coloring method: {}\n"
                "use {} instead: {}".format(
                    coloring, ColorMethod.__name__, ColorMethod.__members__
                )
            )
        res[i, j] = color

    res = pyramid_reduce(res, multichannel=True)

    return res
