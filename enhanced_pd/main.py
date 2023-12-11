r"""
Author: Haoze Pang 23

Description
-----------
This module provide a pandas accessor,'b'  with additional features.

Classes
-------
EnhancedData: pd's dataframe accessor('stat')
"""
import numpy as np
import pandas as pd
from .plotter import PlotMixin
from .cruve_fit import CurveFitMixin
from icecream import ic


# stat for statistic mode: a pandas accessor providing additional features about statistics
@pd.api.extensions.register_dataframe_accessor('stat')
class EnhancedData(CurveFitMixin, PlotMixin):
    """A customised df providing additional plotting and curve fitting features

    It uses plotting capabilities provided by PlotMixin.
    It uses curve fitting capabilities provided by CurveFitMixin.

    Attributes
    ----------
    name: str
        Name of this table
    model:
        The function that predicts y given x.

    x, y, and err_y are just for internal references

    Methods
    -------
    inspect_err_y
    filter_outliers
    """

    def __init__(self, pandas_df):
        """Initiates the class"""

        self._df = pandas_df

        self.model = None
        self.name = 'My Data'

        self._max_col = 3  # maximum number of column this extension currently work with

        self._validate()

    def _validate(self):
        """Validates if the number of columns in the data is less than _max_col"""
        if self._df.shape[1] > self._max_col:
            raise TypeError(f'This is a basic frame. '
                            f'The column of data should be less then {self._max_col}. '
                            f'Your data has {self._df.shape[1]} columns.')

    def inspect_err_y(self):
        """Inspect if the uncertainty on y is positive.

        If not, crop and retain positive uncertainties

        Returns
        -------
         a new data frame without outliers with positive uncertainty values

        """
        if self._df.shape[1] == 3:
            # ensure err_y is positive
            return self._df[self._df.iloc[:, 2] > 0]
        else:
            raise TypeError('This error on y is not well defined. '
                            'Please check the number of column in your data.')

    def filter_outliers(self):
        """Filter outliers outside 1.25 standard deviation away from mean

        Returns
        -------
        a new data frame without outliers
        """

        # getting mean and standard deviation
        mean = self.y.mean()
        standard_deviation = self.y.std()

        # filter
        mask = np.abs(self.y - mean) < 1.25 * standard_deviation
        return self._df[mask]

    @property
    def x(self):
        """The first column of the data"""
        return self._df.iloc[:, 0]

    @property
    def y(self):
        """The second column of the data"""
        return self._df.iloc[:, 1]

    @property
    def err_y(self):
        """The third column of the data, the error on y"""

        # check shape
        if self._df.shape[1] == 3:
            return self._df.iloc[:, 2]
        # if this is a two column data, ensure err_y is always None
        else:
            return None
