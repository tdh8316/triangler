import numpy as np
import skimage


def mean(
    img: np.ndarray,
    triangles: np.ndarray,
) -> np.ndarray:
    result = np.zeros(
        (2 * img.shape[0], 2 * img.shape[1], img.shape[2]),
        dtype=np.uint8,
    )

    for tri in triangles:
        i, j = skimage.draw.polygon(
            r=2 * tri[:, 0],
            c=2 * tri[:, 1],
            shape=result.shape,
        )
        values = img[skimage.draw.polygon(tri[:, 0], tri[:, 1], img.shape)]
        result[i, j] = np.mean(values, axis=0)

    return result
