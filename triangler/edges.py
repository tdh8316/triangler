import enum
from enum import Enum
from typing import Union

import numba
import numpy as np
import skimage.restoration
from numpy.core.multiarray import ndarray
from scipy.signal import convolve2d
from skimage import img_as_float64, img_as_ubyte
from skimage.color import rgb2gray, rgb2lab
from skimage.filters import scharr, gaussian
from skimage.filters.rank import entropy
from skimage.morphology import disk, dilation

from triangler.sampling import (
    SampleMethod,
    poisson_disk_sample,
    threshold_sample,
)


class EdgeMethod(Enum):
    CANNY = enum.auto()
    ENTROPY = enum.auto()
    SOBEL = enum.auto()


class EdgePoints(object):
    __slots__ = ["width", "height", "edge_detector", "num_of_points", "edge_method"]

    def __init__(self, img: ndarray, n: int, edge: EdgeMethod):
        self.width = img.shape[0]
        self.height = img.shape[1]

        self.edge_detector: EdgeDetectors = EdgeDetectors(img)

        self.num_of_points = n

        self.edge_method: EdgeMethod = edge

    def get_edge_points(self, sampling: SampleMethod, blur: int = None) -> ndarray:
        """
        Retrieves the triangle points using Sobel | Canny | Threshold Edge Detection
        """
        if self.edge_method is EdgeMethod.CANNY:
            if blur is None:
                raise ValueError(
                    "To use Canny Edge Detector, you must call this method with (SampleMethod, int)"
                )
            edges = self.edge_detector.canny(blur)
        elif self.edge_method is EdgeMethod.ENTROPY:
            edges = self.edge_detector.entropy()
        elif self.edge_method is EdgeMethod.SOBEL:
            edges = self.edge_detector.sobel()
        else:
            raise ValueError(
                "Unexpected edge processing method: {}\n"
                "use {} instead: {}".format(
                    self.edge_method, SampleMethod.__name__, SampleMethod.__members__
                )
            )

        if sampling is SampleMethod.POISSON_DISK:
            sample_points = poisson_disk_sample(self.num_of_points, edges)
        elif sampling is SampleMethod.THRESHOLD:
            sample_points = threshold_sample(self.num_of_points, edges, 0.2)
        else:
            raise ValueError(
                "Unexpected sampling method: {}\n"
                "use {} instead: {}".format(
                    sampling, SampleMethod.__name__, SampleMethod.__members__
                )
            )

        corners = np.array(
            [
                [0, 0],
                [0, self.height - 1],
                [self.width - 1, 0],
                [self.width - 1, self.height - 1],
            ]
        )
        return np.append(sample_points, corners, axis=0)


class EdgeDetectors(object):
    __slots__ = ["img"]

    def __init__(self, img: ndarray):
        self.img: ndarray = img

    @numba.jit(parallel=True, fastmath=True)
    def sobel(self) -> ndarray:
        _img_as_float = self.img.astype(np.float)
        c: Union[int, float]
        _, _, c = _img_as_float.shape
        _img = (
            0.2126 * _img_as_float[:, :, 0]
            + 0.7152 * _img_as_float[:, :, 1]
            + 0.0722 * _img_as_float[:, :, 2]
            if c > 1
            else _img_as_float
        )

        kh = np.array(
            [
                [-1, -2, 0, 2, 1],
                [-4, -8, 0, 8, 4],
                [-6, -12, 0, 12, 6],
                [-4, -8, 0, 8, 4],
                [-1, -2, 0, 2, 1],
            ],
            dtype=np.float,
        )
        kv = np.array(
            [
                [1, 4, 6, 4, 1],
                [2, 8, 12, 8, 2],
                [0, 0, 0, 0, 0],
                [-2, -8, -12, -8, -2],
                [-1, -4, -6, -4, -1],
            ],
            dtype=np.float,
        )

        gx = convolve2d(_img, kh, mode="same", boundary="symm")
        gy = convolve2d(_img, kv, mode="same", boundary="symm")

        g = np.sqrt(gx * gx + gy * gy)
        g *= 255.0 / np.max(g)

        return g

    @numba.jit(fastmath=True)
    def entropy(self, bal=0.1) -> ndarray:
        dn_img = skimage.restoration.denoise_tv_bregman(self.img, 0.1)
        img_gray = rgb2gray(dn_img)
        img_lab = rgb2lab(dn_img)

        entropy_img = gaussian(
            img_as_float64(dilation(entropy(img_as_ubyte(img_gray), disk(5)), disk(5)))
        )
        edges_img = dilation(
            np.mean(
                np.array([scharr(img_lab[:, :, channel]) for channel in range(3)]),
                axis=0,
            ),
            disk(3),
        )

        weight = (bal * entropy_img) + ((1 - bal) * edges_img)
        weight /= np.mean(weight)
        weight /= np.amax(weight)

        return weight

    @numba.jit(parallel=True, fastmath=True)
    def canny(self, blur: int) -> ndarray:
        # gray_img = rgb2gray(self.img)
        # return cv2.Canny(gray_img, self.threshold, self.threshold*3)

        threshold = 3 / 256
        gray_img = rgb2gray(self.img)
        blur_filt = np.ones(shape=(2 * blur + 1, 2 * blur + 1)) / ((2 * blur + 1) ** 2)
        blurred = convolve2d(gray_img, blur_filt, mode="same", boundary="symm")
        edge_filt = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        edge = convolve2d(blurred, edge_filt, mode="same", boundary="symm")
        for idx, val in np.ndenumerate(edge):
            if val < threshold:
                edge[idx] = 0
        dense_filt = np.ones((3, 3))
        dense = convolve2d(edge, dense_filt, mode="same", boundary="symm")
        dense /= np.amax(dense)

        return dense
