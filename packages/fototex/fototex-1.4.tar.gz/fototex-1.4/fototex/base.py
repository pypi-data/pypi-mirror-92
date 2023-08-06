# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
import itertools
import multiprocessing as mp
import os
from functools import wraps

import numpy as np
from abc import abstractmethod

from fototex import MAX_NB_OF_SAMPLED_FREQUENCIES, NB_PCA_COMPONENTS, R_SPECTRA_NO_DATA_VALUE, \
    _ISOTROPIC_R_SPECTRA_AXIS, _ISOTROPIC_NB_SAMPLE_AXIS, _ANISOTROPIC_R_SPECTRA_AXIS, \
    _ANISOTROPIC_NB_SAMPLE_AXIS, MAX_NB_SECTORS
from fototex._numba import get_sector_directions, get_valid_values
from fototex._tools import mp_r_spectra, mp_h5_r_spectra, normal_pca, \
    h5_incremental_pca, h5_pca_transform, h5_incremental_pca_sector, \
    normal_pca_sector, mp_h5_r_spectra_sector, mp_r_spectra_sector, pca_transform
from fototex.exceptions import FotoBaseError
from fototex.io import H5File, H5TempFile
from fototex.utils import lazyproperty, check_string, check_type, isdir


def boolean(setter):

    @wraps(setter)
    def _bool(self, value):
        try:
            check_type(value, bool)
        except TypeError:
            raise FotoBaseError("'%s' must be boolean but is: '%s'" %
                                (setter.__name__, type(value).__name__))
        output = setter(self, value)

    return _bool


def directory(setter):

    @wraps(setter)
    def _directory(self, path):
        if not isdir(path):
            raise FotoBaseError("'%s' must be a valid directory path" % setter.__name__)
        output = setter(self, path)

    return _directory


def integer(setter):

    @wraps(setter)
    def _integer(self, value):
        try:
            check_type(value, int)
        except TypeError:
            raise FotoBaseError("'%s' must be an integer value but is: '%s'" %
                                (setter.__name__, type(value).__name__))
        output = setter(self, value)

    return _integer


def odd(setter):

    @wraps(setter)
    def _odd(self, value):
        if value % 2 == 0:
            raise FotoBaseError("'%s' must be an odd value (=%d)" % (setter.__name__, value))
        output = setter(self, value)

    return _odd


def positive(setter):

    @wraps(setter)
    def _positive(self, value):
        if value <= 0:
            raise FotoBaseError("'%s' must be positive (=%d)" % (setter.__name__, value))
        output = setter(self, value)

    return _positive


class FotoBase:
    """ Foto base class

    Main Foto abstract class for all Foto subclasses
    """
    _r_spectra = None
    _r_spectra_reduced = None
    _in_memory = None
    _keep_dc_component = None
    _method = None
    _out_dir = None
    _normalized = None
    _standardized = None
    _window_size = None

    data_chunk_size = None
    max_nb_sampled_frequencies = MAX_NB_OF_SAMPLED_FREQUENCIES
    nb_pca_components = NB_PCA_COMPONENTS
    no_data_value = R_SPECTRA_NO_DATA_VALUE
    nb_sampled_frequencies = None
    eigen_vectors = None

    r_spectra_axis = _ISOTROPIC_R_SPECTRA_AXIS
    nb_sample_axis = _ISOTROPIC_NB_SAMPLE_AXIS

    def _compute_pca(self, *args, **kwargs):
        if self.in_memory:
            self.eigen_vectors, self._r_spectra_reduced = normal_pca(self)
        else:
            self.eigen_vectors = h5_incremental_pca(self, *args, **kwargs)

    def _compute_r_spectra(self, nb_processes, *args, **kwargs):
        if self.in_memory:
            self._r_spectra = mp_r_spectra(self, nb_processes)
        else:
            mp_h5_r_spectra(self, nb_processes)

    def compute_pca(self, standardized=True, at_random=False,
                    batch_size=None, max_iter=1000, *args, **kwargs):
        """ Compute PCA for r-spectra tables

        Description
        -----------
        Reduce dimensionality of r-spectra table, with
        respect to number of components (by default set
        to 3 for RGB maps calculation), by applying
        principal component analysis (PCA)

        Parameters
        ----------
        standardized : bool
            if True, standardize r-spectrum data before PCA (subtract mean and divide by std)
        at_random: bool
            apply random incremental pca
        batch_size: int
            size of batch for random incremental pca if at_random=True
        max_iter: int
            maximum number of iterations if at_random=True

        Returns
        -------
        FotoBase:
            the current instance
        """
        self.standardized = standardized
        self._compute_pca(at_random, batch_size, max_iter)

    def compute_r_spectra(self, window_size, nb_sampled_frequencies=None, normalized=False,
                          keep_dc_component=False, nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Compute r-spectra over image with respect to sliding window method

        Description
        -----------
        Compute rspectra tables for given image,
        depending on the selected sliding window
        method and other parameters (window size,
        standardization, etc.)

        Parameters
        ---------
        window_size: int
            size of window
        nb_sampled_frequencies: int
            number of sampled frequencies (optional)
        normalized: bool
            if True, divide by window variance
        keep_dc_component: bool
            keep the DC component (0 frequency) of the FFT. Use carefully as it may
            substantially change the final results!
        nb_processes: int
            number of processes for multiprocessing calculation

        Returns
        -------
        FotoBase:
            the current instance with r-spectra that have been computed
        """
        # Set window size and standardize bool
        self.window_size = window_size
        self.normalized = normalized
        self.keep_dc_component = keep_dc_component

        if not nb_sampled_frequencies:
            self.nb_sampled_frequencies = min(max(int(window_size / 2), 3),
                                              self.max_nb_sampled_frequencies)
        else:
            self.nb_sampled_frequencies = nb_sampled_frequencies

        self._compute_r_spectra(nb_processes)

    def fit_transform(self, other, nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Apply eigen vectors from other Foto object to current object's R-spectra

        Description
        -----------
        Use the PCA eigen vectors retrieved from
        another FotoBase class that has been run
        in order to get reduced r-spectra for the
        current instance

        Examples
        --------

        Parameters
        ----------
        other : FotoBase
            FotoBase class instance that have been run
        nb_processes : int
            number of processes to open for multiprocessing

        Returns
        -------
        FotoBase:
            the current instance
        """
        # TODO: prototype method (apply eigen vectors computed from some image to another)

        # Compute r-spectra and project in input Foto eigenvector's base
        self.compute_r_spectra(other.window_size,
                               nb_sampled_frequencies=other.nb_sampled_frequencies,
                               normalized=other.normalized,
                               nb_processes=nb_processes)

        if self.in_memory:
            self._r_spectra_reduced = pca_transform(self, other)
        else:
            h5_pca_transform(self, other)

    @abstractmethod
    def get_window_generator(self):
        pass

    def run(self, window_size, nb_sampled_frequencies=None, standardized=True, normalized=False,
            keep_dc_component=False, at_random=False, batch_size=None, max_iter=1000,
            nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Run FOTO algorithm

        Description
        -----------
        Run the whole FOTO algorithm, consisting
        in computing r-spectra and applying PCA,
        with respect to window size and corresponding
        method ("block" or "moving window")

        Parameters
        ----------
        window_size : int
            size of the window for 2-D FFT (must be an odd number when method = "moving")
        nb_sampled_frequencies : int
            number of sampled frequencies (if None, is inferred)
        standardized : bool
            if True, standardize r-spectrum data before PCA
        normalized : bool
            if True, divide power spectrum density by window's variance
        keep_dc_component : bool
            either keep or not the DC component (0 frequency) part of the signal FFT. Use it
            carefully as it may change substantially the final results !
        nb_processes: int
            number of processes for parallelization
        at_random: bool
            if True, use random incremental pca
        batch_size: int
            size of batch for random incremental pca (if None, batch size is inferred)
        max_iter: int
            maximum number of iterations when using random incremental PCA

        Examples
        --------
        >>> FotoBase.run(window_size=11, keep_dc_component=True)
        >>> FotoBase.run(window_size=15, standardized=False, normalized=True)

        Returns
        -------
        FotoBase :
            the current instance
        """
        self.compute_r_spectra(window_size,
                               nb_sampled_frequencies,
                               normalized,
                               keep_dc_component,
                               nb_processes)
        self.compute_pca(standardized, at_random, batch_size, max_iter)

    def save_eigen_vectors(self):
        """ Save eigen vectors computed with PCA

        Description
        -----------
        Write eigen vectors retrieved from PCA
        to csv file

        Returns
        -------
        """
        np.savetxt(self.path + "eigen_vectors.csv", self.eigen_vectors, delimiter=',')

    def save_r_spectra(self):
        """ Save r-spectra table to h5 file

        Description
        -----------
        Write computed r-spectra to H5 file

        Returns
        -------
        """
        h5file = H5File(self.path + "rpsectra.h5")
        if self.in_memory:
            h5file.create_dataset("r-spectra", shape=self._r_spectra.shape)
            h5file.append("r-spectra", self._r_spectra)
        else:
            h5file.copy(self.h5, "r-spectra")

        h5file.close()

    @property
    def chunk_size(self):
        return int(self.data_chunk_size / self.nb_sampled_frequencies)

    @lazyproperty
    def h5(self):
        if not self.in_memory:
            return H5TempFile()

    @property
    def in_memory(self):
        return self._in_memory

    @in_memory.setter
    @boolean
    def in_memory(self, value):
        self._in_memory = value

    @property
    def keep_dc_component(self):
        return self._keep_dc_component

    @keep_dc_component.setter
    @boolean
    def keep_dc_component(self, value):
        self._keep_dc_component = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        try:
            self._method = check_string(value, {'block', 'moving_window'})
        except (TypeError, ValueError) as e:
            raise FotoBaseError("Invalid sliding window method: '%s'" % value)

    @property
    @abstractmethod
    def nb_windows(self):
        pass

    @property
    @abstractmethod
    def gdal_no_data_value(self):
        pass

    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    @directory
    def out_dir(self, path):
        self._out_dir = path

    @property
    def path(self):
        return os.path.join(self.out_dir, f"method={self.method}_wsize={self.window_size}_")

    @property
    def mean(self):
        if self.in_memory:
            return get_valid_values(self._r_spectra, self.no_data_value).mean(axis=0)
        else:
            return self.h5["r-spectra"].attrs['mean']

    @property
    def normalized(self):
        return self._normalized

    @normalized.setter
    @boolean
    def normalized(self, value):
        self._normalized = value

    @property
    def std(self):
        if self.in_memory:
            return get_valid_values(self._r_spectra, self.no_data_value).std(axis=0)
        else:
            return self.h5["r-spectra"].attrs['std']

    @property
    def r_spectra(self):
        if self.in_memory:
            return self._r_spectra
        else:
            return self.h5["r-spectra"]

    @property
    def r_spectra_reduced(self):
        if self.in_memory:
            return self._r_spectra_reduced
        else:
            return self.h5["r-spectra-reduced"]

    @property
    def standardized(self):
        return self._standardized

    @standardized.setter
    @boolean
    def standardized(self, value):
        self._standardized = value

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    @integer
    @odd
    @positive
    def window_size(self, value):
        self._window_size = value


class Batch(FotoBase):
    """ Batch abstract class

    Description
    -----------
    Batch is used to allow the FOTO algorithm
    to be applied from multiple image batches.
    This class should not be used, but be
    inherited by subclasses that must implement
    the batch process, especially by using
    multiple inheritance
    """

    foto_instances = None

    def get_window_generator(self):
        w_gen = []
        for foto in self.foto_instances:
            w_gen.append(foto.get_window_generator())

        return itertools.chain(*w_gen)

    @property
    @abstractmethod
    def gdal_no_data_value(self):
        pass

    @property
    def nb_windows(self):
        nb_rspec = 0
        for foto in self.foto_instances:
            nb_rspec += foto.nb_windows
        return nb_rspec


class Sector(FotoBase):
    """ Sector abstract method to implement anisotropy within FOTO algorithm

    Note
    ----
    In order to correctly override FotoBase and use Sector with
    other subclasses of FotoBase, we must keep the constructor
    syntax order. That is to put "nb_sectors" at the end. In case
    we later use multiple inheritance, it is very important so that
    there is no conflict between multiple constructors inheriting
    from the same superclass (here FotoBase)
    """

    nb_sectors = None
    start_sector = None
    r_spectra_axis = _ANISOTROPIC_R_SPECTRA_AXIS
    nb_sample_axis = _ANISOTROPIC_NB_SAMPLE_AXIS
    max_nb_sectors = MAX_NB_SECTORS

    def _compute_pca(self, *args, **kwargs):
        if self.in_memory:
            self.eigen_vectors, self._r_spectra_reduced = normal_pca_sector(self)
        else:
            self.eigen_vectors = h5_incremental_pca_sector(self, *args, **kwargs)

    def _compute_r_spectra(self, nb_processes, *args, **kwargs):
        if self.in_memory:
            self._r_spectra = mp_r_spectra_sector(self, nb_processes)
        else:
            self._r_spectra = mp_h5_r_spectra_sector(self, nb_processes)

    def save_eigen_vectors(self):
        """ Save eigen vectors from PCA decomposition

        Description
        -----------

        Returns
        -------
        :return:
        """
        for path, eigen_vectors in zip(self.path, self.eigen_vectors):
            np.savetxt(path + "eigen_vectors.csv", eigen_vectors, delimiter=',')

    @property
    def chunk_size(self):
        return int(self.data_chunk_size / (self.nb_sampled_frequencies * self.nb_sectors))

    @lazyproperty
    def sectors(self):
        return get_sector_directions(self.nb_sectors, self.start_sector) * 180 / np.pi

    @abstractmethod
    def get_window_generator(self):
        pass

    @property
    @abstractmethod
    def nb_windows(self):
        pass
