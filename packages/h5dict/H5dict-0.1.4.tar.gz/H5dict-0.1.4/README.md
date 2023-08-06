# H5dict

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![Release](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Release&query=%24[0].name&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fnanogennari%252Fh5dict%2Frepository%2Ftags&style=flat-square)](https://gitlab.com/nanogennari/h5dict/)


An interface to read/write HDF5 files as if they where dictionaries.

## Instalation

h5dict can be installed with pip:

    python -m pip install h5dict

### Manual instalation

Clone the repository and run setup.py:

    git clone https://gitlab.com/nanogennari/h5dict.git
    cd h5dict
    python setup.py install

## Usage

Usage example:

    import h5dict
    import numpy as np

    hdf5 = h5dict.File("file.hdf5", "r+")
    hdf5["test_1"] = np.arange(100)
    hdf5["test_2"] = {
        "names": ["Alice", "Bob"],
        "ages": [30, 25]
    }

    for keys in hdf5["test_2"]["names"].keys()
        print(hdf5["test_2"]["names"][key])

    hdf5.close()

## Documentation

Documentation can be found [here](https://nanogennari.gitlab.io/h5dict).