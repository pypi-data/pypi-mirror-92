"""
    SETUP
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SeismicFold",
    version="0.0.2",
    author="Piotr Synowiec",
    author_email="psynowiec@gmail.com",
    description="Calculates fold from SPS data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mysiar/seismic-fold-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
