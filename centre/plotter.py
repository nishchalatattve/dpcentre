"""
Dependencies
------------
    - io.py (same dir)

    - matplotlib
    - sns

Contents
--------
    - custom_plot: decorator
    - save_as: func
"""
import matplotlib.pyplot as plt
import seaborn as sns

from .io import *


def custom_plot(func):
    r"""
    A decorator for plots

    Description
    -----------
    - Enables LaTeX rendering:
        - \usepackage{mathpazo}
        - \usepackage{euler}
        - \usepackage{amsmath}

    - Uses sns style
    - save plot using the second argument of func

    Parameters
    ----------
    func : func
        The function to wrap.

    Dependencies
    ------------
    - The second parameter of func must be the plot_name of the plot you wish to save.
    """

    def wrapper(*args, **kwargs):
        # - initialise
        sns.set()

        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = (r'\usepackage{mathpazo}'
                                               r'\usepackage{euler}'
                                               r'\usepackage{amsmath}')
        plt.rcParams['font.family'] = 'serif'

        # - function call
        plot_name = args[1]
        indicate(f'Plotting {plot_name}...')
        result = func(*args, **kwargs)

        # - save plot
        indicate(f'saving plot "{plot_name}.png"...')
        plt.tight_layout(pad=2.0)
        plt.savefig(f'{plot_name}', dpi=DPI)
        indicate('Plot saved!\n')
        return result

    return wrapper


def save_plot_as(plot_name):
    indicate(f'saving plot "{plot_name}.png"...')
    plt.tight_layout(pad=2.0)
    plt.savefig(f'{plot_name}', dpi=800)
