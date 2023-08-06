# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import numpy as np

from itertools import chain, islice

from sklearn.decomposition import PCA

from fototex import R_SPECTRA_NO_DATA_VALUE
from fototex._numba import sector_average, azimuthal_average, zero_padding, only_contains


def degrees_to_cardinal(d):
    """ Convert degrees to cardinal direction

    Thanks to https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    :param d:
    :return:
    """
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]


def get_slice_along_axis(ndim, axis, _slice):
    """ Used to make indexing with any n-dimensional numpy array

    :param ndim: number of dimensions
    :param axis: axis for which we want the slice
    :param _slice: the required slice
    :return:
    """
    slc = [slice(None)] * ndim
    slc[axis] = _slice

    return tuple(slc)


def get_power_spectrum_density(window, normalized):
    """ Compute power spectrum density for given window

    Description
    -----------

    Parameters
    ----------
    window: numpy.ndarray
        2D window
    normalized: bool
        either divide by window variance or not

    Returns
    -------
    """
    # Fast Fourier Transform (FFT) in 2 dims,
    # center fft and then calculate 2D power spectrum density
    ft = np.fft.fft2(window, norm="ortho")
    ft = np.fft.fftshift(ft)
    psd = np.abs(ft) ** 2

    if normalized:
        psd /= np.var(window)

    return psd


def pca(data, n_components):
    """ Principal component analysis

    :param data: normalized data array
    :param n_components: number of dimensions for PCA
    :return:
    """

    # replace nodata and inf values and standardize
    # data = np.nan_to_num(data)
    # Standardization (mean=0 and std=1)

    # if sklearn_pca:
    sk_pca = PCA(n_components=n_components)
    sk_pca.fit(data)

    return sk_pca.components_.T, sk_pca.transform(data)


def rspectrum(window, radius, window_size, nb_sample, normalized, keep_dc_component, no_data_value):
    """ Compute r-spectrum for given window and filter smaller ones and the ones with no data

    Description
    -----------
    Calculate the azimuthally averaged 1D power
    spectrum (also called radial spectrum, i.e. r-spectrum)

    Parameters
    ----------
    window: numpy.ndarray
        window array
    radius: numpy.ndarray
        corresponding radius integer
    window_size: int
        window typical size
    nb_sample: int
        number of frequencies to sample within window
    normalized: bool
        divide r-spectrum by window variance
    keep_dc_component: bool
        either keep DC component of the FFT (0 frequency part of the signal) or not. It
        may substantially change the results, so use it carefully.
    no_data_value: int or float
        value corresponding to no data

    Returns
    -------
    numpy.ndarray:
        array of isotropic r-spectra
    """
    if window.shape[0] == window.shape[1] == window_size \
            and not only_contains(window, no_data_value):
        if no_data_value:
            window = zero_padding(window, no_data_value)
        if keep_dc_component:
            return azimuthal_average(radius,
                                     get_power_spectrum_density(window, normalized))[0:nb_sample]
        else:
            return azimuthal_average(radius,
                                     get_power_spectrum_density(window,
                                                                normalized))[1:nb_sample + 1]
    else:
        return np.full(nb_sample, R_SPECTRA_NO_DATA_VALUE)


def rspectrum_per_sector(window, radius, sectors, window_size, nb_sample,
                         nb_sectors, normalized, keep_dc_component, no_data_value):
    """ Compute r-spectrum for each sector

    Description
    -----------

    Calculate radial spectrum in specific directions, i.e. quadrants

    Parameters
    ----------

    window: numpy.array
        window
    radius:
    sectors: numpy.array
        result from get_sectors function
        (divide the circle into sectors according to nb_sectors)
    window_size: int
        window typical size
    nb_sample: int
        number of frequencies to sample within window
    nb_sectors: int
        number of sectors
    normalized: bool
        divide r-spectrum by window variance
    keep_dc_component: bool
        either keep DC component of the FFT (0 frequency part of the signal) or not. It
        may substantially change the results, so use it carefully.
    no_data_value: int
        value corresponding to no data

    Returns
    -------
    """
    if window.shape[0] == window.shape[1] == window_size \
            and not only_contains(window, no_data_value):
        if no_data_value:
            window = zero_padding(window, no_data_value)
        if keep_dc_component:
            return sector_average(get_power_spectrum_density(window, normalized),
                                  radius, sectors, nb_sectors)[:, 0:nb_sample]
        else:
            return sector_average(get_power_spectrum_density(window, normalized),
                                  radius, sectors, nb_sectors)[:, 1:nb_sample + 1]
    else:
        return np.full((nb_sectors, nb_sample), R_SPECTRA_NO_DATA_VALUE)


def split_into_chunks(iterable, size=10):
    """

    :param iterable:
    :param size: size of each chunk
    :return:
    """
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def standard_deviation(nb_data, sum_of_values, sum_of_square_values):
    """ Compute standard deviation based on variance formula

    :param nb_data: (int) number of data
    :param sum_of_values:
    :param sum_of_square_values:
    :return:
    """
    return np.sqrt(sum_of_square_values / nb_data - (sum_of_values / nb_data) ** 2)


def standardize(data):
    """ Standardize data (subtract mean and divide by std)

    """
    return (data - data.mean(axis=0)) / data.std(axis=0)
