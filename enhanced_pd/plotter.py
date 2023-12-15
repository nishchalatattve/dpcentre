"""

Functions
---------
plot_init
save_plot

Classes
-------
PlotMixin

"""
import matplotlib.pyplot as plt


def custom_plot(func):
    def wrapper(*args, **kwargs):
        # initialise
        print("Plotting...")

        # use solarize-light style
        plt.style.use('Solarize_Light2')

        # enable LaTeX rendering and apply costume font
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = (r'\usepackage{mathpazo}'
                                               r'\usepackage{euler}'
                                               r'\usepackage{amsmath}')
        plt.rcParams['font.family'] = 'serif'

        # custom plot process
        func(*args, **kwargs)

        # save plot
        save_as = args[0]
        print(f'saving plot {save_as}...')
        plt.tight_layout(pad=4.0)
        plt.savefig(f'{save_as}', dpi=1000)
        print(f'Plot {save_as} saved!\n')


# noinspection PyUnresolvedReferences
class PlotMixin:
    r"""A mixin class providing plotting ability for 'b'

    Methods
    -------
    plot:
        Plot the graph given x and y.
    """

    def _main_plot(self, ax):
        """Draw the main plot"""

        # usual drawing process
        if self.err_y is None:

            ax.plot(self.x, self.y, 'o', markersize=0.5, label='data')
        # different drawing process for plots with error bar
        else:

            ax.errorbar(self.x, self.y, yerr=self.err_y,
                        marker='.',
                        markersize=1,
                        linestyle='None',
                        linewidth=0.5,  # Error bar line width
                        capsize=1,  # Capsize for error bars
                        alpha=0.8,
                        label='data')

    @custom_plot
    def plot(self, save_as: str, caption=''):
        """Create a plot

        Parameters
        ----------
        caption: str
            The caption of the plot, default as an empty string
        save_as: str
            The file name you wish to save your plot as
        """

        # draw data on graph

        # plot best-fit line
        if self.y_predict is not None:

            # configure plot size
            fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [40, 1]},
                                           figsize=(10, 8))

            # plotting original data
            self._main_plot(ax1)

            # plotting best fit curve
            ax1.plot(self.x, self.y_predict, label='fitted curve')

            # adding caption
            ax2.axis('off')
            ax2.text(0.5, 0.5, self._caption_text, ha='center', va='center')

        # follow usual plotting procedure
        else:
            fig, ax1 = plt.subplots(figsize=(8, 6))
            self._main_plot(ax1)

        # caption
        fig.text(0.5, 0.025, caption, ha='center', wrap=True, fontsize=10)

        # legend, label and title
        ax1.legend()

        ax1.set_xlabel(self._df.columns[0])
        ax1.set_ylabel(self._df.columns[1])

        # different name for a plot with a best-fit curve
        if self.y_predict is not None:
            ax1.set_title(f'{self.name}-fitted curve')
        else:
            ax1.set_title(f'{self.name}')
