import enum

from triangler.samplers.poisson import poisson_disk_sampling, PoissonDiskConfig
from triangler.samplers.threshold import threshold_sampling, ThresholdConfig


@enum.unique
class Sampler(enum.Enum):
    POISSON_DISK = "poisson_disk"
    THRESHOLD = "threshold"
