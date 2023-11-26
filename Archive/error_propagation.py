import numpy as np
from icecream import ic


class Errors:
    def __init__(self, err_a, err_b=0, a=0, b=0):
        # input
        self.err_a = err_a
        self.err_b = err_b
        self.a = a
        self.b = b
        # output
        self.err_z = float


class AddError(Errors):
    def __init__(self, err_a, err_b=0, a=0, b=0):
        super().__init__(err_a=err_a, err_b=err_b, a=a, b=b)
        self._calculate()

    def _calculate(self):
        z_square = self.err_a ** 2 + self.err_b ** 2
        self.err_z = np.sqrt(z_square)


class MultiplyError(Errors):
    def __init__(self, err_a, err_b=0, a=0, b=0):
        super().__init__(err_a=err_a, err_b=err_b, a=a, b=b)
        self._calculate()

    def _calculate(self):
        z_square = self.err_a ** 2 + self.err_b ** 2
        self.err_z = np.sqrt(z_square)
        ic(f"the error from multiplication is {self.err_z}")



class LnError(Errors):
    def __init__(self, err_a, err_b=0, a=0, b=0):
        super().__init__(err_a=err_a, err_b=err_b, a=a, b=b)
        self._calculate()

    def _calculate(self):
        self.err_z = self.err_a / self.a
