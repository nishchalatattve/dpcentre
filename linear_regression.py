"""
TODO: None
"""
import numpy as np
import matplotlib.pyplot as plt
from .plot import try_plot
from icecream import ic


class InputData:
    def __init__(self, dataframe):
        # Check if the dataframe has at least three columns
        if dataframe.shape[1] < 3:
            raise ValueError("The dataframe should have at least three columns.")

        # Unpack the first three columns assuming they are x_i, y_i, and err_y
        x_i, y_i, err_y = dataframe.iloc[:, 0], dataframe.iloc[:, 1], dataframe.iloc[:, 2]

        # data
        self.x_i = np.array(x_i)
        self.y_i = np.array(y_i)
        self.err_y = np.array(err_y)
        self.w_i = 1 / self.err_y ** 2
        self.n = len(self.x_i)

        self.validate_input()

    def validate_input(self):
        self.check_dimension()

        # Validate that err_y does not contain zero to avoid division by zero
        if any(self.err_y == 0):
            raise ValueError("Error values must be non-zero to avoid division by zero.")

    def check_dimension(self):
        """
        Check if (x, y) and (y, err_y) are of the same dimension
        """

        if len(self.x_i) != len(self.y_i):
            raise ValueError("x and y must be of the same dimension")

        if len(self.y_i) != len(self.w_i):
            raise ValueError("y and err_y must be of the same dimension")


class Calculation(InputData):

    def __init__(self, dataframe):
        InputData.__init__(self, dataframe)
        # m
        self.gradient = float
        self.err_gradient = float
        # c
        self.intercept = float
        self.err_intercept = float
        # reduced chi square
        self.reduced_chi_square = float
        # calculation
        self.calculate()

    def calculate(self):
        # Preparation 1
        a = np.sum(self.w_i)
        b = np.sum(self.w_i * self.x_i)
        c = np.sum(self.w_i * self.y_i)
        d = np.sum(self.w_i * self.x_i ** 2)
        e = np.sum(self.w_i * self.x_i * self.y_i)
        f = np.sum(self.w_i * self.y_i ** 2)

        # Preparation 2
        D = d - (1 / a) * b ** 2
        E = e - (1 / a) * b * c
        F = f - (1 / a) * c ** 2

        # m&err_m
        self.gradient = E / D
        var_m = (1 / (self.n - 2)) * ((D * F - E ** 2) / (D ** 2))
        # ic(var_m)
        self.err_gradient = np.sqrt(np.abs(var_m))

        # c
        mean_x = b / a
        mean_y = c / a
        self.intercept = mean_y - self.gradient * mean_x
        # reduced chi square
        chi_square = np.sum(self.w_i * (self.y_i - self.gradient * self.x_i - self.intercept) ** 2)
        degrees_of_freedom = (self.n - 2)
        self.reduced_chi_square = chi_square / degrees_of_freedom


class Results(Calculation):
    def __init__(self, dataframe):
        Calculation.__init__(self, dataframe)

    def show_result(self):
        print(f"m = {self.gradient: .5e}")
        print(f"err_m = {self.err_gradient: .5e}")
        print(f"reduced chi square is {self.reduced_chi_square: .5e}")

    def plot_graph(self, x_label='x', y_label='y', title='lsfr plot'):
        # plotting
        plt.figure()
        best_fit_y = self.gradient * self.x_i + self.intercept

        plt.plot(self.x_i, best_fit_y, label='best fit line')
        plt.errorbar(self.x_i, self.y_i, yerr=self.err_y)

        # labels legends and titles
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend()

        plt.savefig(f'plots/{title}.jpg')


lsfr = lambda data: Results(data)
