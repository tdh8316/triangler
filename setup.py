from setuptools import setup

setup(
    name="triangler",
    version="0.1",
    packages=["triangler"],
    url="https://github.com/tdh8316/triangler",
    license="MIT License",
    author="Donghyeok Tak",
    author_email="tdh8316@naver.com",
    description="Convert images to Low-Poly art using Delaunay triangulation.",
    install_requires=["scikit-image", "numpy", "scipy", "numba", "imageio"],
)
