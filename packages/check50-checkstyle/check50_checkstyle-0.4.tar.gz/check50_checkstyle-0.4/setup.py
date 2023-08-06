#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="check50_checkstyle",
    version="0.4",
    author="Patrick Totzke",
    author_email="patricktotzke@gmail.com",
    description="A check50 extension that wraps around "
                "the static code analyser checkstye(.org)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pazz/check50_checkstyle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'check50',
    ],
    package_data={'check50_checkstyle': ['lib/*.jar']},
)
