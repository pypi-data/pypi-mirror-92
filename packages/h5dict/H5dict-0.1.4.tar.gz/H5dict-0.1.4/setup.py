import setuptools
from h5dict import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="H5dict", # Replace with your own username
    version=version,
    author="nano",
    author_email="me@nngn.net",
    description="An interface to read/write HDF5 files as if they where dictionaries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nanogennari.gitlab.io/h5dict/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "h5py",
    ],
)