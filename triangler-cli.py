import timeit

from imageio import imsave

import triangler.process
from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod

op = input("IMAGE PATH:")
sp = input("SAVE AS:")

e = EdgeMethod[input(f"EDGING{EdgeMethod.__members__}[SOBEL]").upper() or "SOBEL"]
b = int(input("BLUR[2]:") or 2)
s = SampleMethod[
    input(f"SAMPLING{SampleMethod.__members__}[POISSON_DISK]:").upper() or "POISSON_DISK"
    ]
p = int(input("POINTS[1000]:") or 1000)
c = ColorMethod[input(f"COLORING{ColorMethod.__members__}[CENTROID]:").upper() or "CENTROID"]

start = timeit.default_timer()
imsave(
    sp,
    triangler.process.process(path=op, coloring=c, sampling=s, blur=b, points=p, edging=e),
)

print("Completed in {}s".format(timeit.default_timer() - start))
