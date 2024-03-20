import numpy as np
import skimage


def centroid(
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
        values = np.mean(tri, axis=0, dtype=np.uint32)
        result[i, j] = img[tuple(values)]

    return result

