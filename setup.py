#!/usr/bin/env python
import os
import sys
import setuptools


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit(0)


setuptools.setup(
    name="django-raw-api",
    version="0.1.0",
    description="JSON API should be as simple as `dict` and status code :)",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imbolc/django-raw-api",
    packages=["raw_api"],
    author="Imbolc",
    author_email="imbolc@imbolc.name",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,
)
