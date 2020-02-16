from argparse import ArgumentParser

from triangler import process


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
        "--edge-detector",
        help="Pre-processing method to use.",
        type=str,
        default="entropy",
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

    process.main(
        path=args.image,
        coloring=args.color,
        sampling=args.sample,
        edging=args.edge_detector,
        points=args.points,
    )
