import logging
import multiprocessing
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import List

from triangler import Triangler
from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.sampling import SampleMethod


# noinspection PyProtectedMember
def main() -> None:
    # noinspection PyTypeChecker
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("images", help="Source files", nargs="+", type=str)
    parser.add_argument(
        "-o", "--output", help="Destination file", nargs="+", type=str, default=None
    )
    parser.add_argument(
        "-s",
        "--sample",
        help="Sampling method for candidate points.",
        type=str.upper,
        default="THRESHOLD",
        choices=SampleMethod._member_names_,
    )
    parser.add_argument(
        "-e",
        "--edge",
        help="Pre-processing method to use.",
        type=str.upper,
        default="SOBEL",
        choices=EdgeMethod._member_names_,
    )
    parser.add_argument(
        "-b",
        "--blur",
        help="Blur radius for approximate canny edge detector.",
        type=int,
        default=2,
        required=False,
    )
    parser.add_argument(
        "-c",
        "--color",
        help="Coloring method for rendering.",
        type=str.upper,
        default="CENTROID",
        choices=ColorMethod._member_names_,
    )
    parser.add_argument(
        "-p", "--points", help="Points threshold.", type=int, default=1024
    )
    parser.add_argument(
        "-l",
        "--reduce",
        help="Apply pyramid reduce to result image",
        action="store_true",
    )

    parser.add_argument(
        "-v", "--verbose", help="Set logger level as DEBUG", action="store_true"
    )

    args = parser.parse_args()

    # Set logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="[%(asctime)s][%(levelname)s] in %(funcName)s(): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    logging.info("Options:{}".format(args))

    if hasattr(args, "output") and isinstance(args.output, list):
        if len(args.images) != len(args.output):
            raise IndexError(
                "The input and output lengths do not match. (input: {}, output: {})".format(
                    len(args.images), len(args.output),
                )
            )

    _e = EdgeMethod[args.edge.upper()]

    if _e is EdgeMethod.CANNY:
        if args.blur < 0:
            raise ValueError("Blur value must be positive integer.")
    else:
        if args.blur != 2:
            raise UserWarning("`--blur` option has no effect except in the case of using Canny Edge Detector.")

    # TODO: Recognize wildcard

    t = Triangler(
        edge_method=_e,
        color_method=ColorMethod[args.color.upper()],
        sample_method=SampleMethod[args.sample.upper()],
        points=args.points,
        blur=args.blur,
        pyramid_reduce=args.reduce,
    )

    # Use multiprocessing to process multiple files at the same time
    _processes: List[multiprocessing.Process] = []
    for index, image in enumerate(args.images):
        _process = multiprocessing.Process(
            target=t.convert_and_save,
            args=(
                image,
                args.output if not isinstance(args.output, list) else args.output[index],
                True,
            ),
        )
        _process.daemon = True
        _processes.append(_process)
        _process.start()

    for process in _processes:
        process.join()
