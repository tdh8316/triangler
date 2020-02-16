import enum
from enum import Enum

import numba


class SampleMethod(Enum):
    __dict__ = ("POISSON_DISK", "THRESHOLD", "RANDOM")

    POISSON_DISK = enum.auto()
    THRESHOLD = enum.auto()
    RANDOM = enum.auto()


@numba.jit(parallel=True)
def random_sample(w: int, h: int, n: int):
    raise NotImplementedError(w, h, n)
