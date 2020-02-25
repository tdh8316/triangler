import multiprocessing
from typing import List

from triangler.cmd import spawn
from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod

images: list = input("IMAGE PATH(Split by comma):").split(",")
# sp = input("SAVE AS:")

# noinspection PyProtectedMember
e = EdgeMethod[input(f"EDGING{EdgeMethod._member_names_}[SOBEL]").upper() or "SOBEL"]
b = int(input("BLUR[2]:") or 2)
# noinspection PyProtectedMember
s = SampleMethod[
    input(f"SAMPLING{SampleMethod._member_names_}[POISSON_DISK]:").upper()
    or "POISSON_DISK"
]
p = int(input("POINTS[1024]:") or 1024)
# noinspection PyProtectedMember
c = ColorMethod[
    input(f"COLORING{ColorMethod._member_names_}[CENTROID]:").upper() or "CENTROID"
]

# Use multiprocessing to process multiple files at the same time
calls: List[multiprocessing.Process] = []
for index, image in enumerate(images):
    image_tri: str = (
        str().join(image.split(".")[:-1]) + "_tri." + image.split(".")[-1]
    )
    _process = multiprocessing.Process(
        target=spawn, args=(image, image_tri, c, s, e, p),
    )
    calls.append(_process)
    _process.daemon = True
    _process.start()
    print("{}. Start process {} to {}".format(index, image, image_tri))

for func in calls:
    func.join()

print("All done!")
