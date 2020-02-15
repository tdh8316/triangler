import enum
from enum import Enum


class ColorMethod(Enum):
    __dict__ = ("MEAN", "CENTROID")

    MEAN = enum.auto()
    CENTROID = enum.auto()
