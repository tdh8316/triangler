from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as rq:
    install_requires = rq.readlines()

setup(
    name="triangler",
    version="0.5",
    packages=["triangler"],
    url="https://github.com/tdh8316/triangler",
    license="MIT License",
    author="Donghyeok Tak",
    author_email="tdh8316@naver.com",
    description="Convert images to Low-Poly art using Delaunay triangulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
