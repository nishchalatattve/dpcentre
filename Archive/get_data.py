import numpy as np


class Data:
    """
    An abstract class containing three numpy arrays

    Attributes
    __________
    a: numpy array
    b: numpy array
    c: numpy array
    """

    def __init__(self):
        self.a = np.array([])
        self.b = np.array([])
        self.c = np.array([])


class RawData(Data):
    """
     A class that imports raw data of three columns using numpy.loadtxt.

     Limits
     ______
        This assumes the file is a csv file and data is present in the first row.
        Only works with three columns of data

    """
    """
    Input: file name that contains the data
    Attributes: file_name: (str) name of the file containing data
                raw_data: (3D numpy array) data
                a: (1D numpy array) first column of the data
                b: (1D numpy array) second column of the data
                c: (1D numpy array) second column of the data
    """

    def __init__(self, file_name_input):
        # file name
        super().__init__()
        self.file_name = file_name_input
        # data
        self.raw_data = np.array([])
        # read data
        self._get_data()

    def _get_data(self):
        """
        Read data from the provided file and store columns in respective attributes.
        """
        try:
            self.raw_data = np.loadtxt(fname=self.file_name, skiprows=0, delimiter=',')
            self.a, self.b, self.c = self.raw_data.T
        except Exception as e:
            print(f"Error loading raw data: {e}")