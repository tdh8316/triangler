![Works on my machine](https://img.shields.io/badge/works-on%20my%20machine-green)

[![Python](https://img.shields.io/badge/Python-%203.10-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Stargazers](https://img.shields.io/github/stars/tdh8316/triangler.svg)](https://github.com/tdh8316/triangler/stargazers)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Ftdh8316%2Ftriangler)](https://twitter.com/intent/tweet?text=Convert%20images%20to%20Low-Poly%20art:&url=https%3A%2F%2Fgithub.com%2Ftdh8316%2Ftriangler)

# Overview

📐 Convert images to Low-Poly art using [Delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation).

![sample](images/triangler-monroe.jpg)

## Table of contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Use as a library](#api)
4. [Sample](#sample)
5. [License](#license)

## Installation

You need [Python](https://www.python.org/) 3.10 or higher.

I strongly recommend to use virtual environment such as Anaconda.
You can [download Anaconda here](https://www.anaconda.com/distribution/#download-section).

Follow manual below to create conda virtual environment for Triangler with the Anaconda.

```cmd
$ conda create -n triangler python=3.12
$ activate triangler
(triangler)$ python -m pip install git+https://github.com/tdh8316/triangler/
```

## Usage

```
(triangler)$ python -m triangler -h
positional arguments:
  input                 Input image

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output image name
  -p POINTS, --points POINTS
                        Number of sample points to use
  -e {EdgeDetector.CANNY,EdgeDetector.ENTROPY,EdgeDetector.SOBEL}, --edge-detector {EdgeDetector.CANNY,EdgeDetector.ENTROPY,EdgeDetector.SOBEL}
                        Edge detection algorithm
  -s {Sampler.POISSON_DISK,Sampler.THRESHOLD}, --sampler {Sampler.POISSON_DISK,Sampler.THRESHOLD}
                        Point sampling algorithm
  -r {Renderer.CENTROID,Renderer.MEAN}, --renderer {Renderer.CENTROID,Renderer.MEAN}
                        Color polygon rendering algorithm
  -V, --version         show program's version number and exit
  -d, --debug           Enable debug mode
```

## API

You can also use Triangler as a library.

```python
import triangler

triangler.convert(
    img="INPUT_IMAGE.jpg",
    save_path="OUTPUT_IMAGE.jpg",
)
```

## Sample

### Effect of the number of points

|                Original Image                |                 5000 Points                  |
|:--------------------------------------------:|:--------------------------------------------:|
|         ![sample](images/monroe.jpg)         | ![sample](images/triangler-monroe-5000p.jpg) |
|               **1000 Points**                |                **500 Points**                |
| ![sample](images/triangler-monroe-1000p.jpg) | ![sample](images/triangler-monroe-500p.jpg)  |

### More samples

| Original                    | Triangler                             |
|-----------------------------|---------------------------------------|
| ![sample](images/birds.jpg) | ![sample](images/triangler-birds.jpg) |


## License

Licensed under the MIT License.

Copyright 2024 `Donghyeok Tak`

## Credits

Some algorithms, including the Poisson disk sampling, are based
on [pmaldonado/PyTri](https://github.com/pmaldonado/PyTri).
