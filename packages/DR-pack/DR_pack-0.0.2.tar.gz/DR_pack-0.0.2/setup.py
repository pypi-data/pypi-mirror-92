# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:03:40 2021

@author: MILIND
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DR_pack",
    version="0.0.2",
    author="Riddhi",
    author_email="drpack@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Riddhi-28/DR_pack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)