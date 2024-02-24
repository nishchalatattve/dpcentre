"""
Tools for data analysis
Haoze 24
"""

import numpy as np


def mean_of_std(data):
    if data is not np.ndarray:
        data = np.array(data)

    return np.sqrt(np.sum(data ** 2))
