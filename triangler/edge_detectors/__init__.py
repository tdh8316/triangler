import enum

from triangler.edge_detectors.sobel import sobel, SobelConfig
from triangler.edge_detectors.canny import canny, CannyConfig
from triangler.edge_detectors.entropy import entropy, EntropyConfig


@enum.unique
class EdgeDetector(enum.Enum):
    CANNY = "canny"
    ENTROPY = "entropy"
    SOBEL = "sobel"
