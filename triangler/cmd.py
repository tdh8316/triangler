import multiprocessing
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
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

    args = parser.parse_args()

    calls: List[multiprocessing.Process] = []

    for image in args.images:
        _process = multiprocessing.Process(
            target=spawn,
            args=(
                image,
                None,
                ColorMethod[args.color.upper()],
                SampleMethod[args.sample.upper()],
                EdgeMethod[args.edge.upper()],
                args.points,
            ),
        )
        calls.append(_process)
        _process.start()

    for func in calls:
        func.join()


def spawn(
    img_path: str,
    out_path: str or None,
    c: ColorMethod,
    s: SampleMethod,
    e: EdgeMethod,
    p: int,
) -> None:
    print("Spawned " + img_path)
    start_time = time.time()
    res: ndarray = process(
        path=img_path, coloring=c, sampling=s, edging=e, points=p,
    )

    imsave(
        out_path or (str().join(Path(img_path).name.split(".")[:-1]) + "_tri.jpg"), res
    )
    print("Finished " + img_path + " in {}s".format(time.time() - start_time))
