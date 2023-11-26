"""
TODO: annotation in matplotlib
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from icecream import ic

def linear_model(x, m, c):
    return m*x + c
def polynomial(x, a_0, a_1, a_2, a_3, a_4, x0):
    x = x - x0
    return a_0 + a_1 * x + a_2 * x ** 2 + a_3 * x ** 3 + a_4 * x ** 4


class FitResults:
    def __init__(self):
        self.parameters = None
        self.covariance = None
        self.errors = None
        self.fitted_function = None
        self.reduced_chi_squared = None


class FittingData:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.x = data.iloc[:, 0]
        self.function = data.iloc[:, 1]
        self.err = data.iloc[:, 2] if data.shape[1] == 3 else None


class CurveFit:
    def __init__(self, data: pd.DataFrame, fitting_model, initial_guess=None):
        # Attributes
        self.data_to_fit = FittingData(data)
        self.model = fitting_model
        self.estimate = initial_guess
        self.results = FitResults()

        # methods
        self.fit()
        self.plot()

    # noinspection PyTupleAssignmentBalance
    def fit(self):

        if self.data_to_fit.err is not None:
            self.results.parameters, self.results.covariance = curve_fit(self.model, self.data_to_fit.x,
                                                                         self.data_to_fit.function, p0=self.estimate,
                                                                         sigma=self.data_to_fit.err)
        else:
            self.results.parameters, self.results.covariance = curve_fit(self.model, self.data_to_fit.x,
                                                                         self.data_to_fit.function, p0=self.estimate, )
        self.results.fitted_function = self.model(self.data_to_fit.x, *self.results.parameters)
        self.results.errors = np.sqrt(np.diag(self.results.covariance))

        if self.data_to_fit.err is not None:
            self.calculate_reduced_chi_squared()

    def calculate_reduced_chi_squared(self):

        number_of_data_points = len(self.data_to_fit.x)
        number_of_parameters = len(self.results.parameters)
        degrees_of_freedom = number_of_data_points - number_of_parameters

        chi_squared = sum(((self.results.fitted_function - self.data_to_fit.function) / self.data_to_fit.err) ** 2)
        self.results.reduced_chi_squared = chi_squared / degrees_of_freedom

    def plot(self, title='fitting plot'):
        plt.figure()

        plt.plot(self.data_to_fit.x, self.results.fitted_function, label='fitted curve')
        if self.data_to_fit.err is not None:
            plt.errorbar(self.data_to_fit.x, self.data_to_fit.function, yerr=self.data_to_fit.err,
                         marker='o',
                         markersize=0.3,
                         linewidth=0.3,
                         capsize=0.3,
                         label='original data')
        else:
            plt.plot(self.data_to_fit.x, self.data_to_fit.function, 'ro', markersize=0.5, label='original data')
        plt.xlabel(self.data_to_fit.data.columns[0])
        plt.ylabel(self.data_to_fit.data.columns[1])
        plt.title(title)
        plt.legend()
        plt.savefig(f'plots/{title}.png', dpi=1000)
