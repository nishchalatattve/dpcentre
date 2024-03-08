"""
Data processing centre
Haoze 24

Dependencies
------------
    - pandas
    - scipy

    - plotter.py (same dir)
    - curve_fit.py (same dir)

Contents
--------
    - lab2d: pandas dataframe api extension
    - lab2d_c
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

from .projects_src import indicate
from .plotter import custom_plot

FIGSIZE = (8, 6)
MARKERSIZE = 5
DPI = 800


@pd.api.extensions.register_dataframe_accessor('lab2d')
class Lab2D:
    def __init__(self, pandas_df: pd.DataFrame):
        self.data = pandas_df
        self.name = 'My Data'

        self.num_data = self.data.shape[0]

        self.validate()

    def validate(self):
        """
        Validate the number of columns
        """
        expected_num_cols = 2
        actual_num_cols = self.data.shape[1]

        if actual_num_cols != expected_num_cols:
            raise TypeError(f"Expected number of columns is {expected_num_cols}")

    @property
    def min_point(self):
        arg_min = np.argmin(self.data.iloc[:, 1])
        x_min = self.data.iloc[arg_min, 0]
        y_min = self.data.iloc[arg_min, 1]
        return x_min, y_min

    @property
    def max_point(self):
        return np.max(self.data, axis=0)

    @custom_plot
    def plot(self, save_as='my_plot'):
        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1],
                   marker='o', s=MARKERSIZE, label='experiment data')
        # label and titles
        ax.set_title(self.name)
        ax.set_xlabel(self.data.columns[0])
        ax.set_ylabel(self.data.columns[1])

        return fig, ax


@pd.api.extensions.register_dataframe_accessor('lab2de')
class Lab2DE(Lab2D):
    def __init__(self, pandas_df: pd.DataFrame):
        super().__init__(pandas_df)

    def validate(self):
        """
        Validates the df
        """
        # validate the number of columns
        expected_num_cols = 3
        actual_num_cols = self.data.shape[1]
        if actual_num_cols != expected_num_cols:
            raise TypeError(f"Expected number of columns is {expected_num_cols}")

    @custom_plot
    def plot(self, plot_name='my_plot'):
        fig, ax = plt.subplots(figsize=FIGSIZE)

        ax.errorbar(self.data.iloc[:, 0],
                    self.data.iloc[:, 1],
                    yerr=self.data.iloc[:, 2],
                    marker='o', markersize=MARKERSIZE, label='experiment data',
                    linestyle='None', alpha=0.8, )

        # - label and titles
        ax.set_title(self.name)
        ax.set_xlabel(self.data.columns[0])
        ax.set_ylabel(self.data.columns[1])


@pd.api.extensions.register_dataframe_accessor('lab2d_c')
class Lab2DC(Lab2D):
    """
    Examples
    --------
    """

    # - init
    def __init__(self, pandas_df: pd):
        super().__init__(pandas_df)
        self.model = None
        self.guess = None
        self.caption = ''

    # - curve fitting
    # @property
    # def guess(self):
    #     return mh(self.model, self.data.iloc[:, 0], self.data.iloc[:, 1])

    @property
    def fit_results(self):
        if self.model is None:
            raise ValueError('Please specify a model')
        params, cov = curve_fit(self.model, xdata=self.data.iloc[:, 0], ydata=self.data.iloc[:, 1],
                                p0=self.guess, maxfev=1800)

        return params, cov

    @property
    def parameters(self):
        return self.fit_results[0]

    @property
    def errors(self):
        return np.sqrt(np.diag(self.fit_results[1]))

    @property
    def y_predict(self):
        params = self.fit_results[0]
        result = self.model(self.data.iloc[:, 0], *params)

        return result

    # - plotting
    @custom_plot
    def plot(self, plot_name='my_data'):
        """
        ax1 is the axes of the actual plot
        ax2 is the axes of the caption
        """
        # - init
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                       gridspec_kw={'height_ratios': [40, 1]},
                                       figsize=(10, 8))
        # - plot
        ax1.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1],
                    marker='o', s=MARKERSIZE, label='experiment data')
        ax1.plot(self.data.iloc[:, 0], self.y_predict, color='r', label='fitted curve')
        # - label and titles
        ax1.set_title(self.name)
        ax1.set_xlabel(self.data.columns[0])
        ax1.set_ylabel(self.data.columns[1])
        ax1.legend()
        # - caption
        ax2.axis('off')
        param_info = f'parameters = {self.fit_results[0]}'
        ax2.text(0.5, 0.5, param_info, ha='center', va='center')
        fig.text(0.5, 0.025, self.caption, ha='center', wrap=True, fontsize=10)

    @custom_plot
    def residual_plot(self):
        fig, ax = plt.subplots()


@pd.api.extensions.register_dataframe_accessor('lab2de_c')
class Lab2DEC(Lab2DE, Lab2DC):
    def __init__(self, pandas_df: pd.DataFrame):
        super().__init__(pandas_df)

    @property
    def fit_results(self):
        if self.model is None:
            raise ValueError('Please specify a model')

        params, cov = curve_fit(self.model, xdata=self.data.iloc[:, 0], ydata=self.data.iloc[:, 1],
                                sigma=self.data.iloc[:, 2],
                                p0=self.guess, maxfev=1800)

        return params, cov

    @property
    def chi_squared(self):
        diff = self.y_predict - self.data.iloc[:, 1]
        result = np.sum((diff / self.data.iloc[:, 2]) ** 2)
        return result

    @property
    def reduced_chi_squared(self):
        num_params = len(self.parameters)
        dof = self.num_data - num_params
        result = self.chi_squared / dof
        return result

    @custom_plot
    def plot(self, plot_name='my_data'):
        """
        ax1 is the axes of the actual plot
        ax2 is the axes of the caption
        """
        # - init
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                       gridspec_kw={'height_ratios': [40, 1]},
                                       figsize=(10, 8))
        # - plot
        ax1.errorbar(self.data.iloc[:, 0],
                     self.data.iloc[:, 1],
                     yerr=self.data.iloc[:, 2],
                     marker='o', markersize=MARKERSIZE, label='experiment data',
                     linestyle='None', alpha=0.8, )
        ax1.plot(self.data.iloc[:, 0], self.y_predict, color='r', label='fitted curve')
        # - label and titles
        ax1.set_title(self.name)
        ax1.set_xlabel(self.data.columns[0])
        ax1.set_ylabel(self.data.columns[1])
        ax1.legend()
        # - caption
        ax2.axis('off')
        param_info = f'parameters = {self.fit_results[0]}' + '' + fr'\(\chi^2_r = \) {self.reduced_chi_squared}'
        ax2.text(0.5, 0.5, param_info, ha='center', va='center')
        fig.text(0.5, 0.025, self.caption, ha='center', wrap=True, fontsize=10)
