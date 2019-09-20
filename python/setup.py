# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()

setup(
    # Package
    name="Python_Project_Layout",
    version="0.0",
    packages=find_packages(exclude=("tests")),
    url="https://github.com/aisnes/python-project-template",
    install_requires=[],
    entry_points={
        "console_scripts": ["python-project-layout=app.__main__:main"],
    },
    zip_safe=False,
    
    # Contact
    author="Andreas Isnes Nilsen",
    author_email="andnil94@gmail.com",
    
    # Description
    description="A template for python projects",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
