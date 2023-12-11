r"""
Haoze Pang 23
This module provide a pandas accessor,'b'  with additional features.
"""
import numpy as np
import pandas as pd
from .plotter import PlotMixin
from .cruve_fit import CurveFitMixin
from icecream import ic


# b for Basic: a pandas accessor providing additional features
@pd.api.extensions.register_dataframe_accessor('b')
class BasicData(CurveFitMixin, PlotMixin):
    """A customised df providing additional plotting and curve fitting features

    It uses plotting capabilities provided by PlotMixin.
    It uses curve fitting capabilities provided by CurveFitMixin.

    Attributes
    ----------
    name: str
        Name of this table
    x:
        The first column of the df
    y:
        The second column of the df
    err_y:
        The third column of the df (error on y)
    """

    def __init__(self, pandas_df):
        """Initiates the class"""
        self._df = pandas_df
        self.model = None
        self.name = 'My Data'
        self._max_col = 3  # maximum number of column this df currently work with

        self._validate()

    def _validate(self):
        """Validates if the number of columns in the data is less than _max_col"""
        if self._df.shape[1] > self._max_col:
            raise TypeError(f'This is a basic frame. '
                            f'The column of data should be less then {self._max_col}. '
                            f'Your data has {self._df.shape[1]} columns.')

    @property
    def x(self):
        """The first column of the data"""
        return self._df.iloc[:, 0]

    @x.setter
    def x(self, value):
        """Setter of x"""
        self._df.iloc[:, 0] = value

    @property
    def y(self):
        """The second column of the data"""
        return self._df.iloc[:, 1]

    @y.setter
    def y(self, value):
        """Setter of y"""
        self._df.iloc[:, 1] = value

    @property
    def err_y(self):
        """The third column of the data, the error on y"""

        # check shape
        if self._df.shape[1] == 3:

            # ensure err_y is positive
            self._df = self._df[self._df.iloc[:, 2] > 0]

            # returns the third column of data
            return self._df.iloc[:, 2]
        # if this is a two column data, ensure err_y is always None
        else:
            return None

    @err_y.setter
    def err_y(self, value):
        """Setter of err_y"""
        self._df.iloc[:, 2] = value
