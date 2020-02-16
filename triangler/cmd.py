from argparse import ArgumentParser
from pathlib import Path

from skimage.io import imsave

from triangler import process
from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod


def main():
    parser = ArgumentParser()

    parser.add_argument("image", help="Source file", type=str)
    parser.add_argument("-o", help="Destination file", type=str, default=None)
    parser.add_argument(
        "-s",
        "--sample",
        help="Sampling method for candidate points.",
        type=str,
        default="threshold",
        choices=["poisson_disk", "threshold"],
    )
    parser.add_argument(
        "-e",
        "--edge",
        help="Pre-processing method to use.",
        type=str,
        default="canny",
        choices=["canny", "entropy"],
    )
    parser.add_argument(
        "-c",
        "--color",
        help="Coloring method for rendering.",
        type=str,
        default="centroid",
        choices=["centroid", "mean"],
    )
    parser.add_argument(
        "-p", "--points", help="Points threshold.", type=int, default=4096
    )

    args = parser.parse_args()

    result = process.main(
        path=args.image,
        coloring=ColorMethod[args.color.upper()],
        sampling=SampleMethod[args.sample.upper()],
        edging=EdgeMethod[args.edge_detector.upper()],
        points=args.points,
    )

    imsave(args.o or (Path(args.image).name + "_tri.jpg"), result)
