import timeit

from imageio import imsave

import triangler.process
from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod

op = input("IMAGE PATH:")
sp = input("SAVE AS:")

# noinspection PyProtectedMember
e = EdgeMethod[input(f"EDGING{EdgeMethod._member_names_}[SOBEL]").upper() or "SOBEL"]
b = int(input("BLUR[2]:") or 2)
# noinspection PyProtectedMember
s = SampleMethod[
    input(f"SAMPLING{SampleMethod._member_names_}[POISSON_DISK]:").upper() or "POISSON_DISK"
    ]
p = int(input("POINTS[1000]:") or 1000)
# noinspection PyProtectedMember
c = ColorMethod[input(f"COLORING{ColorMethod._member_names_}[CENTROID]:").upper() or "CENTROID"]

start = timeit.default_timer()
imsave(
    sp,
    triangler.process.process(path=op, coloring=c, sampling=s, blur=b, points=p, edging=e),
)

print("Completed in {}s".format(timeit.default_timer() - start))
