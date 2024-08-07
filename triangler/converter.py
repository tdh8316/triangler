import os
from typing import Union, Optional

import numpy as np
import skimage
from scipy.spatial import Delaunay
from skimage.util import img_as_ubyte

from triangler import edge_detectors, samplers, renderers
from triangler.config import TrianglerConfig
from triangler.edge_detectors import (
    EdgeDetector,
    SobelConfig,
    CannyConfig,
    EntropyConfig,
)
from triangler.renderers import Renderer
from triangler.samplers import Sampler, PoissonDiskConfig, ThresholdConfig


def convert(
    img: Union[np.ndarray, str],
    save_path: Optional[str] = None,
    config: TrianglerConfig = TrianglerConfig(),
    canny_config: CannyConfig = CannyConfig(),
    entropy_config: EntropyConfig = EntropyConfig(),
    sobel_config: SobelConfig = SobelConfig(),
    poisson_disk_config: PoissonDiskConfig = PoissonDiskConfig(),
    threshold_config: ThresholdConfig = ThresholdConfig(),
    reduce: bool = True,
    add_corners: bool = True,
    debug: bool = False,
) -> np.ndarray:
    """
    Convert an image into a low-poly art using the Delaunay triangulation

    Args:
        img (np.ndarray | str): Input image path or array
        save_path (Optional[str]): The path to save the result
        config (TrianglerConfig): Basic converter configuration
        canny_config (CannyConfig): Canny edge detection configuration
        entropy_config (EntropyConfig): Entropy edge detection configuration
        sobel_config (SobelConfig): Sobel edge detection configuration
        poisson_disk_config (PoissonDiskConfig): Poisson disk sampling configuration
        threshold_config (ThresholdConfig): Threshold sampling configuration
        reduce (bool): Reduce the result image size to match the input image
        add_corners (bool): Add the corners of the image to the sample points
        debug (bool): Enable debug mode

    Returns:
        np.ndarray: The low-poly art (result)
    """
    filename: Optional[str] = None
    extension: str
    if isinstance(img, str):
        if debug:
            print(f"[DEBUG] Read image from '{img}'")
        filename = os.path.basename(img)
        extension = filename.split(".")[-1]
        img: np.ndarray = skimage.io.imread(img)
    else:
        extension = "png"
    if debug:
        print(f"[DEBUG] Image extension: {extension}")

    if not isinstance(img, np.ndarray):
        raise ValueError(
            "Invalid input image. "
            + f"Expected str or np.ndarray type but got {type(img)}.",
        )

    if debug:
        print(f"[DEBUG] Image shape: {img.shape}")

    edges: np.ndarray
    if debug:
        print(f"[DEBUG] Edge detection algorithm: {config.edge_detector}")
    match config.edge_detector:
        case EdgeDetector.SOBEL:
            edges = edge_detectors.sobel(img, sobel_config)
        case EdgeDetector.CANNY:
            edges = edge_detectors.canny(img, canny_config)
        case EdgeDetector.ENTROPY:
            edges = edge_detectors.entropy(img, entropy_config)
        case _:
            raise ValueError(
                f"Invalid edge detection algorithm '{config.edge_detector}'. "
                + "Expected one of: "
                + ", ".join([f"'{e.value}'" for e in EdgeDetector]),
            )
    if debug:
        if filename:
            edge_filename = f"edges_{filename}"
        else:
            edge_filename = f"edges.{extension}"
        print(f"[DEBUG] Save edges to '{edge_filename}'")
        skimage.io.imsave(edge_filename, img_as_ubyte(edges))

    sample_points: np.ndarray
    if debug:
        print(f"[DEBUG] Sampling algorithm: {config.sampler}")
    match config.sampler:
        case Sampler.POISSON_DISK:
            sample_points = samplers.poisson_disk_sampling(
                edges,
                n_samples=config.n_samples,
                config=poisson_disk_config,
            )
        case Sampler.THRESHOLD:
            sample_points = samplers.threshold_sampling(
                edges,
                n_samples=config.n_samples,
                config=threshold_config,
            )
        case _:
            raise ValueError(
                f"Invalid sampling algorithm '{config.sampler}'. "
                + "Expected one of: "
                + ", ".join([f"'{s.value}'" for s in Sampler]),
            )

    # Add the corners of the image to the sample points
    if add_corners:
        if debug:
            print("[DEBUG] Add heuristic points to the sample points")
        corners = np.array(
            [
                [0, 0],
                [0, int(img.shape[1] / 2)],
                [0, img.shape[1]],
                [img.shape[0], 0],
                [img.shape[0], int(img.shape[1] / 2)],
                [img.shape[0], img.shape[1]],
                [int(img.shape[0] / 2), int(img.shape[1] / 2)],
            ]
        )
        sample_points = np.concatenate([sample_points, corners], axis=0)

    triangulated: Delaunay = Delaunay(sample_points)
    triangles = sample_points[triangulated.simplices]

    if debug:
        print(f"[DEBUG] Rendering algorithm: {config.renderer}")
    match config.renderer:
        case Renderer.CENTROID:
            result = renderers.centroid(img, triangles)
        case Renderer.MEAN:
            result = renderers.mean(img, triangles)
        case _:
            raise ValueError(
                f"Invalid rendering algorithm '{config.renderer}'. "
                + "Expected one of: "
                + ", ".join([f"'{r.value}'" for r in Renderer]),
            )

    if reduce:
        if debug:
            print("[DEBUG] Resize the result image to match the input image")
        result = skimage.transform.pyramid_reduce(
            result,
            downscale=2,
            channel_axis=-1,
        )
        result = img_as_ubyte(result)

    if save_path:
        if save_path.split(".")[-1] != extension:
            save_path = f"{save_path}.{extension}"
        if debug:
            print(f"[DEBUG] Save the result to '{save_path}'")
        skimage.io.imsave(save_path, result)

    return result
