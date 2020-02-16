# Overview
`Triangler` is a tool to generate Low-Polygon image using [Delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation).

![sample](./docs/m_tri2.jpg)

>**Warning: Triangler is extremely slow, but provide the best result if use Entropy Edge Detection and Poisson Disk Sampling option.**

It takes about 5s-3m.

# Usage
Currently, the interface for end-users is only Command-Line.

```cmd
$ git clone https://github.com/tdh8316/triangler.git
$ python -m pip install setup.py
$ python -m triangler -h
usage: __main__.py [-h] [-o O] [-s {poisson_disk,threshold}]
                   [-e {canny,entropy}] [-c {centroid,mean}] [-p POINTS]
                   image

positional arguments:
  image                 Source file

optional arguments:
  -h, --help            show this help message and exit
  -o O                  Destination file
  -s {poisson_disk,threshold}, --sample {poisson_disk,threshold}
                        Sampling method for candidate points.
                        Default: poisson_disk
  -e {canny,entropy}, --edge {canny,entropy}
                        Pre-processing method to use.
                        Default: entropy
  -c {centroid,mean}, --color {centroid,mean}
                        Coloring method for rendering.
                        Default: centroid
  -p POINTS, --points POINTS
                        Points threshold.
```

## Example command
`$ python -m triangler image.jpg -p=1000`

# Sample
|Original|5000 Points|
|:------:|:---------:|
|![sample](./docs/m.jpg)|![sample](./docs/m_tri.jpg)
|**2500 Points**|**1000 Points**|
|![sample](./docs/m_tri2.jpg)|![sample](./docs/m_tri3.jpg)|

|Original|Processed|
|--------|---------|
|![sample](./docs/parrot.jpg)|![sample](./docs/parrot_tri.jpg)|
|![sample](./docs/yeji2.jpg)|![sample](./docs/yeji2_tri.jpg)|
|![sample](./docs/matt.jpg)|![sample](./docs/matt_tri.jpg)|
|![sample](./docs/sino.jpg)|![sample](./docs/sino_tri.jpg)|

## Acknowledgement
The `Edge Detection` and `Sampling` algorithms are based on [pmaldonado/PyTri](https://github.com/pmaldonado/PyTri/blob/master/delaunay)

## TODO
 - [ ] Sobel
 - [ ] Optimization