import numba
import numpy as np
from numpy.core.multiarray import ndarray
from scipy.signal import convolve2d
from skimage.color import rgb2gray

from triangler.poisson_disk_sampling import poisson_disk_sample
from triangler.sampling import SampleMethod
from triangler.threshold_sampling import threshold_sample


class Point(object):
    def __init__(self, img: ndarray, n: int):
        self.img = img
        self.width = self.img.shape[0]
        self.height = self.img.shape[1]

        self.num_of_points = n
        if self.num_of_points > round(self.width * self.height * 0.5):
            raise UserWarning("The number of points is too large")

    @numba.jit
    def generate(self, blur: int, sampling: SampleMethod) -> ndarray:
        """
        Retrieves the triangle points using Canny Edge Detection
        """
        edges: ndarray = Canny.compute(self.img, blur)

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

        threshold = 2.9 / 256
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
        dense = dense / np.amax(dense)

        return dense
