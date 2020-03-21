import subprocess

from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod

images: list = [x.strip() for x in input("IMAGE PATH(Split by comma):").split(",")]
# sp = input("SAVE AS:")

# noinspection PyProtectedMember
e: str = input(f"EDGING{EdgeMethod._member_names_}[SOBEL]").upper() or "SOBEL"
b: str = input("BLUR[2]:") or "2" if e == EdgeMethod.CANNY.name else "2"
# noinspection PyProtectedMember
s: str = input(
    f"SAMPLING{SampleMethod._member_names_}[POISSON_DISK]:"
).upper() or "POISSON_DISK"

p: str = input("POINTS[1024]:") or str(1024)
# noinspection PyProtectedMember
c: str = input(f"COLORING{ColorMethod._member_names_}[CENTROID]:").upper() or "CENTROID"

subprocess.call(
    [
        *"python -m triangler".split(),
        *images,
        "-e",
        e,
        "-b",
        b,
        "-s",
        s,
        "-p",
        p,
        "-c",
        c,
    ]
)
