from dataclasses import dataclass

from triangler.edge_detectors import EdgeDetector
from triangler.renderers import Renderer
from triangler.samplers import Sampler


@dataclass
class TrianglerConfig:
    n_samples: int = 1024
    edge_detector: EdgeDetector = EdgeDetector.SOBEL
    sampler: Sampler = Sampler.POISSON_DISK
    renderer: Renderer = Renderer.CENTROID
