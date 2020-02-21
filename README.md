# Overview
`Triangler` is a tool to generate Low-Polygon image using [Delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation).

![sample](./docs/m_tri2.jpg)

# Usage
Currently, the interface for end-users is only Command-Line.
```cmd
$ git clone https://github.com/tdh8316/triangler.git
$ python -m pip install -r requirements.txt
$ python triangler-cli.py
```
## Setup
```cmd
$ git clone https://github.com/tdh8316/triangler.git
$ python -m pip install setup.py
$ python -m triangler -h
usage: __main__.py [-h] [-o OUTPUT [OUTPUT ...]] [-s {POISSON_DISK,THRESHOLD}]
                   [-e {CANNY,ENTROPY,SOBEL}] [-c {MEAN,CENTROID}] [-p POINTS]
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
  -c {MEAN,CENTROID}, --color {MEAN,CENTROID}
                        Coloring method for rendering. (default: CENTROID)
  -p POINTS, --points POINTS
                        Points threshold. (default: 1024)
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
|![sample](./docs/wolf.jpg)|![sample](./docs/wolf_tri.jpg)|
|![sample](./docs/parrot.jpg)|![sample](./docs/parrot_tri.jpg)|

# License
Licensed under the **MIT** License.
