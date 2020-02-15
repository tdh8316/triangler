import enum
from enum import Enum


class SampleMethod(Enum):
    __dict__ = ("POISSON_DISK", "THRESHOLD")

    POISSON_DISK = enum.auto()
    THRESHOLD = enum.auto()
