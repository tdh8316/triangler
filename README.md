[![Python](https://img.shields.io/badge/Python-%203.6-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Stargazers](https://img.shields.io/github/stars/tdh8316/triangler.svg)](https://github.com/tdh8316/triangler/stargazers)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Ftdh8316%2Ftriangler)](https://twitter.com/intent/tweet?text=Convert%20images%20to%20Low-Poly%20art:&url=https%3A%2F%2Fgithub.com%2Ftdh8316%2Ftriangler)

# Overview
`Triangler` is a tool to generate Low-Polygon image using [Delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation).

![sample](./docs/m_tri2.jpg)

# Pre-requirements
I strongly recommend to use virtual environment such as PyEnv or Anaconda.
If you don't have Anaconda, [download Anaconda](https://www.anaconda.com/distribution/#download-section)

Follow manual below to create python virtual environment for triangler with Anaconda.
```cmd
$ conda create -n triangler python=3.6
$ activate triangler
(triangler)$ git clone https://github.com/tdh8316/triangler.git
(triangler)$ python -m pip install -r requirements.txt
```

# Usage
Currently, the interface for end-users is only Command-Line.
```cmd
$ activate triangler
(triangler)$ python triangler-cli.py
```
## Setup
```cmd
$ activate triangler
(triangler)$ git clone https://github.com/tdh8316/triangler.git
(triangler)$ python -m pip install setup.py
(triangler)$ python -m triangler -h
usage: __main__.py [-h] [-o OUTPUT [OUTPUT ...]] [-s {POISSON_DISK,THRESHOLD}]
                   [-e {CANNY,ENTROPY,SOBEL}] [-b BLUR] [-c {MEAN,CENTROID}]
                   [-p POINTS] [-l REDUCE] [-v]
                   images [images ...]

positional arguments:
  images                Source files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT [OUTPUT ...], --output OUTPUT [OUTPUT ...]
                        Destination file (default: None)
  -s {POISSON_DISK,THRESHOLD}, --sample {POISSON_DISK,THRESHOLD}
                        Sampling method for candidate points. (default: THRESHOLD)
  -e {CANNY,ENTROPY,SOBEL}, --edge {CANNY,ENTROPY,SOBEL}
                        Pre-processing method to use. (default: SOBEL)
  -b BLUR, --blur BLUR  Blur radius for approximate canny edge detector.
                        (default: 2)
  -c {MEAN,CENTROID}, --color {MEAN,CENTROID}
                        Coloring method for rendering. (default: CENTROID)
  -p POINTS, --points POINTS
                        Points threshold. (default: 1024)
  -l, --reduce          Apply pyramid reduce to result image (default: False)
  -v, --verbose         Set logger level as DEBUG (default: False)
```

The `POISSON_DISK` option is extremely slow, however it can provide the best result.

It takes a minimum of 5 seconds to a maximum of 3 minutes.

## Example command
`$ python -m triangler image.jpg -o output.jpg -s poisson_disk`

# Sample
|Original|5000 Points|
|:------:|:---------:|
|![sample](./docs/m.jpg)|![sample](./docs/m_tri.jpg)
|**2500 Points**|**1000 Points**|
|![sample](./docs/m_tri2.jpg)|![sample](./docs/m_tri3.jpg)|

|Original|Processed|
|--------|---------|
|![sample](./docs/birds.jpg)|![sample](./docs/birds_tri.jpg)|
|![sample](./docs/yeji2.jpg)|![sample](./docs/yeji2_tri.jpg)|
|![sample](./docs/bfly.jpg)|![sample](./docs/bfly_tri.jpg)|
|![sample](./docs/parrot.jpg)|![sample](./docs/parrot_tri.jpg)|

# License
Licensed under the **MIT** License.
