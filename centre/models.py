"""
Common models.
Haoze 24

Dependencies:
------------
    - numpy
"""
import numpy as np


def linear_model(x, m, c):
    return m * x + c


def lorentzian(x, centre, width, normalisation_constant):
    part_b = 0.5 * width
    part_c = (x - centre) ** 2 + (0.5 * width) ** 2
    return normalisation_constant * (part_b / part_c)


def forced_oscillation_amplitude(omega, omega_0, gamma, normalisation_constant):

    part_a = (omega**2 - omega_0**2)**2
    part_b = (gamma*omega)**2
    return normalisation_constant*(1/np.sqrt(part_a + part_b))
