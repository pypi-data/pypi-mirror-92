#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import setuptools

name = "boututils"
root_path = Path(__file__).parent
init_path = root_path.joinpath(name, "__init__.py")
readme_path = root_path.joinpath("README.md")

with readme_path.open("r") as f:
    long_description = f.read()

setuptools.setup(
    name=name,
    author="Ben Dudson et al.",
    description="Python package containing BOUT++ utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boutproject/boututils",
    project_urls={
        "Bug Tracker": "https://github.com/boutproject/boututils/issues/",
        "Documentation": "https://bout-dev.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/boutproject/boututils/",
    },
    packages=setuptools.find_packages(),
    keywords=[
        "bout++",
        "bout",
        "plasma",
        "physics",
        "data-extraction",
        "data-analysis",
        "data-visualization",
    ],
    use_scm_version=True,
    setup_requires=[
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
        "setuptools_scm_git_archive",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "h5py",
        "future",
        "netCDF4",
        "importlib-metadata ; python_version<'3.8'",
    ],
    extras_require={"mayavi": ["mayavi", "PyQt5"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        (
            "License :: OSI Approved :: "
            "GNU Lesser General Public License v3 or later (LGPLv3+)"
        ),
        "Operating System :: OS Independent",
    ],
)
