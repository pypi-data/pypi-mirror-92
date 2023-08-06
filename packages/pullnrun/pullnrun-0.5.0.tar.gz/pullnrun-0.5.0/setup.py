#!/usr/bin/env python3

import re
import setuptools

with open("pullnrun/_version.py", "r") as f:
    try:
        version = re.search(
            r"__version__\s*=\s*[\"']([^\"']+)[\"']",f.read()).group(1)
    except:
        raise RuntimeError('Version info not available')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pullnrun",
    version=version,
    author="Toni Kangas",
    description="A simple python app for running a set of commands from remote sources and pushing result files to remote targets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangasta/pullnrun",
    packages=setuptools.find_packages(),
    package_data={
        'pullnrun': ['schemas/*.yml']
    },
    scripts=["bin/pullnrun"],
    install_requires=[
        "importlib_resources; python_version<'3.7'",
        "jsonschema~=3.0",
        "requests~=2.0",
        "pyyaml~=5.0"
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
