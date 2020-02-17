from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

from skimage.io import imsave

from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.process import process
from triangler.sampling import SampleMethod


# noinspection PyProtectedMember
def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("image", help="Source file", type=str)
    parser.add_argument("-o", help="Destination file", type=str, default=None)
    parser.add_argument(
        "-s",
        "--sample",
        help="Sampling method for candidate points.",
        type=str,
        default="threshold",
        choices=SampleMethod._member_names_,
    )
    parser.add_argument(
        "-e",
        "--edge",
        help="Pre-processing method to use.",
        type=str,
        default="sobel",
        choices=EdgeMethod._member_names_,
    )
    parser.add_argument(
        "-c",
        "--color",
        help="Coloring method for rendering.",
        type=str,
        default="centroid",
        choices=ColorMethod._member_names_,
    )
    parser.add_argument(
        "-p", "--points", help="Points threshold.", type=int, default=4096
    )

    args = parser.parse_args()

    result = process(
        path=args.image,
        coloring=ColorMethod[args.color.upper()],
        sampling=SampleMethod[args.sample.upper()],
        edging=EdgeMethod[args.edge_detector.upper()],
        points=args.points,
    )

    imsave(args.o or (Path(args.image).name + "_tri.jpg"), result)
