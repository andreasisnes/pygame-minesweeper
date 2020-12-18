from os.path import join, dirname
from setuptools import setup, find_packages
from json import load


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()


def metadata(value):
    with open(join(dirname(__file__), "metadata.json")) as f:
        return load(f)[value]


setup(
    # Package
    name="pygame-minesweeper",
    version=metadata("version"),
    packages=find_packages(exclude=("tests", "screenshots")),
    url="https://github.com/andreasisnes/Elitekollektivet.Minesweeper",
    install_requires=[
        "pygame",
        "pygame-minesweeper-core",
        "pygame-minesweeper-sprites",
        "appdirs",
    ],
    entry_points={
        "console_scripts": [
            "minesweeper = minesweeper.__main__:main"
        ],
    },
    zip_safe=False,
    # Contact
    author="Andreas Isnes Nilsen",
    author_email="andreas.isnes@gmail.com",
    # Description
    description="Minesweeper game implemented in python using pygame",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
