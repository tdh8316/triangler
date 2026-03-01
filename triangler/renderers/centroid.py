import numpy as np
import skimage


def centroid(
    img: np.ndarray,
    triangles: np.ndarray,
) -> np.ndarray:
    h, w = img.shape[:2]
    channels = 1 if img.ndim == 2 else img.shape[2]
    result_shape = (2 * h, 2 * w) if channels == 1 else (2 * h, 2 * w, channels)
    result = np.zeros(
        result_shape,
        dtype=np.uint8,
    )

    for tri in triangles:
        i, j = skimage.draw.polygon(
            r=2 * tri[:, 0],
            c=2 * tri[:, 1],
            shape=result.shape[:2],
        )
        center = np.rint(np.mean(tri, axis=0)).astype(np.int64)
        center[0] = np.clip(center[0], 0, h - 1)
        center[1] = np.clip(center[1], 0, w - 1)
        result[i, j] = img[center[0], center[1]]

    return result
