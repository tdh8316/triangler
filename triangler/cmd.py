import logging
import multiprocessing
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import List

from numpy.core.multiarray import ndarray
from skimage.io import imsave

from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.process import process
from triangler.sampling import SampleMethod


# noinspection PyProtectedMember
def main() -> None:
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

    _c = ColorMethod[args.color.upper()]
    _s = SampleMethod[args.sample.upper()]
    _e = EdgeMethod[args.edge.upper()]

    if args.output and len(args.images) != len(args.output):
        raise IndexError

    if _e is EdgeMethod.CANNY and args.blur < 0:
        raise ValueError

    if len(args.images) > 1:
        # Use multiprocessing to process multiple files at the same time
        calls: List[multiprocessing.Process] = []
        for index, image in enumerate(args.images):
            _process = multiprocessing.Process(
                target=spawn,
                args=(
                    image,
                    None if not args.output else args.output[index],
                    _c,
                    _s,
                    _e,
                    args.points,
                    args.reduce,
                ),
            )
            calls.append(_process)
            _process.daemon = True
            _process.start()

        for func in calls:
            func.join()
    else:
        spawn(
            args.images[0],
            None if not args.output else args.output[0],
            _c,
            _s,
            _e,
            args.points,
            args.reduce,
        )


def spawn(
    img_path: str,
    out_path: str or None,
    c: ColorMethod,
    s: SampleMethod,
    e: EdgeMethod,
    p: int,
    r: bool,
) -> None:
    logging.info("Spawned process for {}".format(img_path))
    start_time = time.time()
    res: ndarray = process(
        path=img_path, coloring=c, sampling=s, edging=e, points=p, reduce=r,
    )

    imsave(
        out_path
        or (str().join(img_path.split(".")[:-1]) + "_tri." + img_path.split(".")[-1]),
        res,
    )
    logging.info("Finished {} in {}s".format(img_path, time.time() - start_time))
