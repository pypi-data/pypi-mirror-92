#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="appchance-cli",
    version="0.1.3.2",
    author="Appchance Python Team",
    author_email="backend@appchance.com",
    short_description="Python Backend CLI Toolkit",
    description=(
        "Developers toolkit for Appchance Python backend team."
        "Also spell book for wizards and ninjas - useful in dungeons."),
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/appchance/appchance-tools/",
    packages=setuptools.find_packages(),
    install_requires=["fire==0.3.1", "wheel", "twine"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires=">=3.8",
    scripts=["bin/ace"],
)
