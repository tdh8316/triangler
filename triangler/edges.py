import enum
from enum import Enum

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

from triangler.poisson_disk_sampling import poisson_disk_sample
from triangler.sampling import SampleMethod
from triangler.threshold_sampling import threshold_sample


class EdgeMethod(Enum):
    __dict__ = ("CANNY", "ENTROPY")

    CANNY = enum.auto()
    ENTROPY = enum.auto()


class Point(object):
    def __init__(self, img: ndarray, n: int, edge: EdgeMethod):
        self.img = img
        self.width = self.img.shape[0]
        self.height = self.img.shape[1]

        self.num_of_points = n
        if self.num_of_points > round(self.width * self.height * 0.5):
            raise UserWarning("The number of points is too large")

        self.edge_method: EdgeMethod = edge

    @numba.jit(parallel=True)
    def generate(self, blur: int, sampling: SampleMethod) -> ndarray:
        """
        Retrieves the triangle points using Canny Edge Detection
        """
        edges: ndarray = ...
        if self.edge_method is EdgeMethod.CANNY:
            edges = Canny.compute(self.img, blur)
        elif self.edge_method is EdgeMethod.ENTROPY:
            edges = Entropy.compute(self.img)

        sample_points = None
        if sampling is SampleMethod.POISSON_DISK:
            sample_points = poisson_disk_sample(self.num_of_points, edges)
        elif sampling is SampleMethod.THRESHOLD:
            sample_points = threshold_sample(self.num_of_points, edges, 0.2)

        corners = np.array(
            [
                [0, 0],
                [0, self.height - 1],
                [self.width - 1, 0],
                [self.width - 1, self.height - 1],
            ]
        )
        return np.append(sample_points, corners, axis=0)


class Canny(object):
    @staticmethod
    @numba.jit(parallel=True)
    def compute(img: ndarray, blur: int) -> ndarray:
        # gray_img = rgb2gray(self.img)
        # return cv2.Canny(gray_img, self.threshold, self.threshold*3)

        threshold = 3 / 256
        gray_img = rgb2gray(img)
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


class Entropy(object):
    @staticmethod
    @numba.jit
    def compute(img, bal=0.1) -> ndarray:
        dn_img = skimage.restoration.denoise_tv_bregman(img, 0.1)
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
