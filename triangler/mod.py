from datetime import datetime
from typing import Union

from numpy.core.multiarray import ndarray
from skimage.io import imread
from skimage.io import imsave

from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.process import process
from triangler.sampling import SampleMethod


class Triangler(object):
    """
    Triangler wrapper
    """

    def __init__(
        self,
        edge_method: EdgeMethod = EdgeMethod.SOBEL,
        sample_method: SampleMethod = SampleMethod.THRESHOLD,
        color_method: ColorMethod = ColorMethod.CENTROID,
        points: int = 1000,
        blur: int = 2,
        pyramid_reduce: bool = True,
    ):
        """
        :param edge_method: Edge detecting method
        :param sample_method: Sampling method
        :param color_method: Color transfer method
        :param points: The number of sampling points
        :param blur: Not required if you don't use Canny Edge Detecting
        :param pyramid_reduce: Use pyramid reduce
        """
        self.edge_method: EdgeMethod = edge_method
        self.sample_method: SampleMethod = sample_method
        self.color_method: ColorMethod = color_method
        self.points: int = points
        self.blur: int = blur
        self.pyramid_reduce: bool = pyramid_reduce

    def convert(self, source: Union[str, ndarray]) -> ndarray:
        """
        Return converted image as array
        :param source: An image you'd like to convert.
        :return:
        """
        _type = type(source)
        if _type not in (str, ndarray):
            raise TypeError("Supported type: str, ndarray but {}".format(_type))

        if _type is str:
            source = imread(source)

        return process(
            img=source,
            coloring=self.color_method,
            sampling=self.sample_method,
            edging=self.edge_method,
            points=self.points,
            blur=self.blur,
            reduce=self.pyramid_reduce,
        )

    def save(self, source: Union[str, ndarray], output: str = None, **kwargs) -> None:
        """
        Convert and save the result as image
        :param source: An image you'd like to convert.
        :param output: The name of the result image file.
        :return:
        """
        _is_source_string: bool = isinstance(source, str)
        _out = output or (
            "Triangler_{}.jpg".format(datetime.now().strftime("%H-%M-%b-%d-%G"))
            if not _is_source_string
            else (str().join(source.split(".")[:-1]) + "_tri." + source.split(".")[-1])
        )
        if kwargs["print_log"]:
            print(
                "Converting {}{}...".format(
                    "" if not _is_source_string else (source + " -> "), _out
                )
            )
        imsave(
            _out, self.convert(source),
        )

        if kwargs["print_log"]:
            print("Saved {}".format(_out))
