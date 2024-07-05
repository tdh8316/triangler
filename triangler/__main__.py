import argparse
from os.path import basename, dirname

import triangler
from triangler import EdgeDetector, Sampler, Renderer, TrianglerConfig


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input", type=str, help="Input image")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output image name",
    )

    parser.add_argument(
        "-p",
        "--points",
        type=int,
        default=1024,
        help="Number of sample points to use",
    )
    parser.add_argument(
        "-e",
        "--edge-detector",
        type=str,
        default=EdgeDetector.SOBEL,
        choices=[e.value for e in EdgeDetector],
        help="Edge detection algorithm",
    )
    parser.add_argument(
        "-s",
        "--sampler",
        type=str,
        default=Sampler.POISSON_DISK,
        choices=[s.value for s in Sampler],
        help="Point sampling algorithm",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        type=str,
        default=Renderer.CENTROID,
        choices=[r.value for r in Renderer],
        help="Color polygon rendering algorithm",
    )
    parser.add_argument(
        "-l",
        "--reduce",
        action="store_true",
        help="Reduce the result image size to match the input image",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"triangler {triangler.__version__}",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    triangler_config = TrianglerConfig(
        n_samples=args.points,
        edge_detector=EdgeDetector(args.edge_detector),
        sampler=Sampler(args.sampler),
        renderer=Renderer(args.renderer),
    )

    triangler.convert(
        args.input,
        (args.output or f"{dirname(args.input)}/triangler-{basename(args.input)}"),
        config=triangler_config,
        reduce=args.reduce,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()
