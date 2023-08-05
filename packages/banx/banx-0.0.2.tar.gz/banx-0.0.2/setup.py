import setuptools
from pathlib import Path

setuptools.setup(
    name="banx",
    version="0.0.2",
    long_description="This package contains my secret message",
    packages=setuptools.find_packages(exclude=["data", "test"])
)
