import enum

from triangler.renderers.centroid import centroid
from triangler.renderers.mean import mean


@enum.unique
class Renderer(enum.Enum):
    CENTROID = "centroid"
    MEAN = "mean"
