import numpy as np
import skimage


def mean(
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
        src_i, src_j = skimage.draw.polygon(
            r=tri[:, 0],
            c=tri[:, 1],
            shape=img.shape[:2],
        )
        values = img[src_i, src_j]
        if values.size == 0:
            continue
        result[i, j] = np.mean(values, axis=0)

    return result
