# -*- coding: utf-8 -*-

from os import environ
from os.path import join, dirname
from setuptools import setup, find_packages


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()

setup(
    # Package
    name=environ["PROJECT_NAME"],
    version="0.0",
    packages=find_packages(exclude=("tests")),
    url="https://github.com/aisnes/minesweeper",
    install_requires=[],
    entry_points={
        "console_scripts": ["minesweeper=app.__main__:main"],
    },
    zip_safe=False,
    
    # Contact
    author="Andreas Isnes Nilsen",
    author_email="andnil94@gmail.com",
    
    # Description
    description="Minesweeper implementation in Python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
