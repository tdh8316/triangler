import numba
import numpy as np
from imageio import imread
from numpy.core.multiarray import ndarray
from scipy.spatial import Delaunay
from skimage.draw import polygon
from skimage.transform import pyramid_reduce

from triangler.color import ColorMethod
from triangler.edges import EdgePoints, EdgeMethod
from triangler.sampling import SampleMethod


@numba.jit(fastmath=True, parallel=True)
def process(
    path: str,
    coloring: ColorMethod,
    sampling: SampleMethod,
    edging: EdgeMethod,
    points: int,
    blur: int = 2,
) -> np.array:
    img: ndarray = imread(path)
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

    # return pyramid_reduce(res, multichannel=True)
    return res
