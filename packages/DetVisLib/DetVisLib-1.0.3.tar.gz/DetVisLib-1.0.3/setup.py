# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 20:15:16 2021

@author: Andro
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="DetVisLib",
    version="1.0.3",
    description="Detections Visualization Library - easy to use library to visualize detections from various object detection frameworks.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Andropogon/DetVisLib",
    author="Jan Gąsienica-Józkowy",
    author_email="jgjozkowy@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["detvislib"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "detvislib=detvislib.__main__:main",
        ]
    },
)