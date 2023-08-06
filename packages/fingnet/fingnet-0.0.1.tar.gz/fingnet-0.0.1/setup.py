import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="fingnet",
    version="0.0.1",
    author="Meyer",
    description="This package will be available soon!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fingnetwork",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)