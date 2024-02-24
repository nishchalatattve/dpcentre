"""
A script for propagating errors
Haoze 24
"""
import numpy as np


def multiply_error(a, b, err_a, err_b):
    error = np.sqrt((err_a / a) ** 2 + (err_b / b) ** 2)
    return error
