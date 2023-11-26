"""
Data analysis module
====================

    This is a package containing some useful modules for data analysis.

Requirements
------------
    Python 3.12 or higher
    numpy
    matplotlib

Features
________
    Others
    ------
        A class containing other useful methods for data analysis

    LSFR
    ----
        A class containing best fit gradient and intercepts for linear chi-square regression

    Error
    _____
        An abstract class that have attributes useful for propagating error. Concrete example is substantiated with
    child classes like AddError.

"""
import numpy as np
from scipy.ndimage import gaussian_filter1d


def local_maximum(function):
    """
    Find the local maximum of a function
    Parameters
    ----------
    function: array like objects

    Returns
    -------
    numpy array
        the function containing the maximum value of the input function
    """

    maximum = []
    for i in range(1, len(function) - 1):
        if function[i - 1] < function[i] and function[i] > function[i + 1]:
            maximum.append(function[i])

    return np.array(maximum)


def local_minimum(function):
    """
    Find the local minimum of a function
    Parameters
    ----------
    function: array like objects

    Returns
    -------
    numpy array
        the function containing the minimum value of the input function
    """
    minimum = []
    index = []
    for i in range(1, len(function) - 1):
        if function[i - 1] > function[i] and function[i] < function[i + 1]:
            minimum.append(function[i])
            index.append(i)

    return np.array(minimum)


def improved_local_maximum(data, sigma=1, threshold=None, min_distance=1):
    """
    Find the local maximum of a noisy signal.

    Parameters
    ----------
    data : array_like
        The input signal.
    sigma : float, optional
        The standard deviation of the Gaussian kernel used in smoothing.
    threshold : float, optional
        The value above which a peak will be considered a true peak.
    min_distance : int, optional
        The minimum number of data points separating peaks.

    Returns
    -------
    maxima_indices : numpy array
        The indices of the local maxima in the input data.
    """

    # Smooth the data using a Gaussian filter to reduce noise
    smoothed_data = gaussian_filter1d(data, sigma=sigma)

    # Find local maxima using a comparison with neighbors
    maxima_indices = []
    last_maxima_index = -min_distance - 1  # Initialize to satisfy the min_distance condition initially
    for i in range(1, len(smoothed_data) - 1):
        if smoothed_data[i - 1] < smoothed_data[i] > smoothed_data[i + 1]:
            if (threshold is None or smoothed_data[i] > threshold) and (i - last_maxima_index > min_distance):
                maxima_indices.append(i)
                last_maxima_index = i

    return np.array(maxima_indices)
