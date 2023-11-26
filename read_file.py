import pandas as pd
import matplotlib.pyplot as plt


class RawData:
    """
    A class that reads a csv file.

    Parameters
    _________
    file_name: str
        Name of the csv file. The first row of the csv file is treated as column names, not data


    Attributes
    __________
    data :pd.DataFrame

    """

    def __init__(self, file_name):
        # attributes
        self.file = file_name
        self.data = None
        # methods
        self.read_data()
        self.filter_outliers()

    def read_data(self):
        """
        Delete blotted data points and convert all data points to float
        """
        data = pd.read_csv(self.file)
        # Attempt to convert all data to float; invalid entries will become NaN
        data = data.apply(pd.to_numeric, errors='coerce')
        # Remove rows with NaN values (previously invalid data points)
        refined_data = data.dropna()

        self.data = refined_data
        #  Delete data points where the error is invalid.
        if self.data.shape[1] == 3:
            self.data = self.data[self.data.iloc[:, 2] > 0]

    def crop(self, value_range, column_to_crop=0):
        lower_bound, upper_bound = value_range
        # Create a boolean mask where the x-values are between lower bound and upper bound
        mask = (self.data.iloc[:, column_to_crop] >= lower_bound) & (self.data.iloc[:, column_to_crop] <= upper_bound)
        self.data = self.data[mask]

    def filter_outliers(self):
        target_column = self.data.iloc[:, 1]
        mean = target_column.mean()
        std = target_column.std()
        mask = (target_column - mean) < 1 * std
        self.data = self.data[mask]

    def try_plot(self):
        plt.figure()
        plt.plot(self.data.iloc[:, 0], self.data.iloc[:, 1], 'ro', markersize=0.5)
        plt.xlabel(self.data.columns[0])
        plt.ylabel(self.data.columns[1])
        plt.title('initial plot')
        plt.savefig('plots/initial_plot.png')



