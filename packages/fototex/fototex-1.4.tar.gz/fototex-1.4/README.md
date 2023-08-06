# Fourier Transform Textural Ordination in Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/fototex.svg)](https://badge.fury.io/py/fototex)

Freely adapted from https://github.com/CaussesCevennes/FOTO.py

## List of authors
* Benjamin Pillot <benjamin.pillot@ird.fr>
* Dominique Lyszczarz <observatoire@causses-et-cevennes.fr>
* Claire Teillet <teillet.claire@hotmail.com>
* Pierre Couteron <pierre.couteron@ird.fr>
* Nicolas Barbier <nicolas.barbier@ird.fr>
* Philippe Verley <philippe.verley@ird.fr>
* Marc Lang <marc.lang@irstea.fr>
* Thibault Catry <thibault.catry@ird.fr>
* Laurent Demagistri <laurent.demagistri@ird.fr>
* Nadine Dessay <nadine.dessay@ird.fr>

## Tutorial
See [here](https://nbviewer.jupyter.org/urls/framagit.org/benjaminpillot/fototex/-/raw/master/tutorial.ipynb)


## Description
FOTO (Fourier Textural Ordination) is an algorithm allowing texture
characterization and comparison, and is fully
described in _Textural ordination based on Fourier spectral 
decomposition: a method to analyze and compare landscape patterns_
(Pierre Couteron, Nicolas Barbier and Denis Gautier, 2006)


## Installation
Use `pip` in a terminal to install fototex:
```shell script
$ pip install fototex
```

### Note on GDAL
Installing GDAL through `pip` might be tricky as it only gets
the bindings, so be sure the library is already installed on 
your machine, and that the headers are located in the right
folder. Another solution may to install it through a third-party
distribution such as `conda`.


## Usage

### In memory against HDF5

* Regarding computation performances, in case you have a strong machine
with extended memory, or if you have small images to treat, you can
implement the algorithm "in memory":
```python
from fototex.foto import Foto
foto = Foto("path/to/your/image", method='block', band=1, in_memory=True)
foto.run(window_size=11)
```

* Otherwise, in case of large images or a limited machine, it is possible
to implement the algorithm with HDF5 data storage. In that case, Foto 
runs an incremental PCA, that you may customize, assisted with HDF5 
storage:
```python
from fototex.foto import Foto
foto = Foto("path/to/your/image", method="moving_window", in_memory=False, data_chunk_size=40000)
foto.run(window_size=11)
```

The argument ``data_chunk_size`` gives information on the reading/writing 
rate to h5 files.

### DC component
When computing the R-spectra, you may keep the DC 
component of the FFT, such as:
```python
from fototex.foto import Foto
foto = Foto("path/to/your/image", method="moving_window", in_memory=False, data_chunk_size=40000)
foto.run(window_size=11, nb_sample=5, keep_dc_component=True)
```
In that case, it is important to keep in mind that R will
range from 0 to nb_sample - 1 (in the example, 
R=0, 1, 2, 3, 4). Otherwise, it will range from 1 to 
nb_sample (here, R=1, 2, 3, 4, 5).

### Normalize
If you want to normalize the values of the power spectrum 
over the image (dividing by the variance of each given window),
you may add the option (False by default):
```python
from fototex.foto import Foto
foto = Foto("path/to/your/image", method="moving_window", in_memory=False, data_chunk_size=40000)
foto.run(window_size=11, normalized=True)
```
