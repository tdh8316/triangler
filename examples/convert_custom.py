"""Edit the paths and settings below, then run this script with Triangler installed."""

import triangler
from triangler import EdgeDetector, Renderer, Sampler, TrianglerConfig
from triangler.edge_detectors import CannyConfig
from triangler.samplers import PoissonDiskConfig

INPUT_IMAGE = "INPUT_IMAGE.jpg"
OUTPUT_IMAGE = "OUTPUT_IMAGE.jpg"

config = TrianglerConfig(
    # More sample points generally produce smaller triangles and finer detail.
    n_samples=2048,
    edge_detector=EdgeDetector.CANNY,
    sampler=Sampler.POISSON_DISK,
    renderer=Renderer.MEAN,
)

# These settings apply when edge_detector is EdgeDetector.CANNY.
canny_config = CannyConfig(
    # RGB weights used to convert the image to grayscale; keep their sum at 1.
    r_weight=0.2126,
    g_weight=0.7152,
    b_weight=0.0722,
    # Larger sigma values smooth the image more before detecting edges.
    sigma=2.0,
    # Lower thresholds retain weaker edges; keep low_threshold <= high_threshold.
    low_threshold=0.1,
    high_threshold=0.2,
)

poisson_disk_config = PoissonDiskConfig(
    # More candidate attempts per point can improve coverage, but take longer.
    n_iter=32,
    # Small positive value added to edge weights to avoid division by zero.
    eps=1e-6,
)

triangler.convert(
    img=INPUT_IMAGE,
    save_path=OUTPUT_IMAGE,
    config=config,
    canny_config=canny_config,
    poisson_disk_config=poisson_disk_config,
    reduce=True,  # Match the input size; False keeps twice the width and height.
    add_corners=True,  # Include image corners to cover the image boundaries.
    debug=False,  # True prints progress and saves edges_<input name> in the cwd.
)
