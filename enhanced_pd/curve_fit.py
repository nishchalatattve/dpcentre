r"""
Author: Haoze Pang 23

Description
------------
This module provide a mixin class for curve fitting. It is designed to work with pandas accessor
'stat'.

Function
---------
mh

Class
-----
CurveFitMixin
"""
import inspect
from functools import cache, cached_property
import numpy as np
from scipy.optimize import curve_fit


def mh(model, x, y_actual, sigma=1):
    r"""Metropolis-Hasting algorithm

    An algorithm providing initial guess on the best fit parameters using the Metropolis algorithm.

    Warnings
    --------
    This does not work well with Breit–Wigner equation.

    Parameters
    ----------
    model:
        The model used to predict y values.
    x:
        Independent variable.
    y_actual:
        The y value from experiment.
    sigma:
        The error on y. Default to None.

    Returns
    -------
    mean_params:
        An array of best fit parameters using Metropolis algorithm

    """
    print('Guessing best-fit parameters ... ')
    num_trials = 50000  # The number of simulations performed.

    # assign the standard deviation of our data
    std = sigma

    # get the number of fitting parameters from model
    num_params = len(inspect.signature(model).parameters) - 1

    def ln_likelihood(params):
        """
        Returns the ln of likelihood of seeing this parameter assuming the parameter
        distribution follows gaussian.
        """

        # generate the ln of gaussian
        y_predicted = model(x, *params)

        numerator = (y_actual - y_predicted) ** 2
        denominator = 2 * std ** 2

        return np.sum(-(numerator / denominator))

    def acceptance_probability():
        """The probability that we shall accept the sample"""
        return np.exp(ln_likelihood(current_sample) - ln_likelihood(previous_sample))

    accepted_samples = []
    previous_sample = np.zeros(num_params)
    # sampling
    for _ in range(num_trials):

        # generate a sample centred at the previous sample
        current_sample = np.random.normal(previous_sample, 1)

        if np.random.uniform(0, 1) < acceptance_probability():
            # accept this sample
            accepted_samples.append(current_sample)

            # move one step forward in the markov chain
            # for the next sample, the current sample is the previous sample
            previous_sample = current_sample

    # discard burn ins
    burn_in_ratio = 0.5
    burn_ins = int(burn_in_ratio * len(accepted_samples))
    accepted_samples = accepted_samples[burn_ins:]

    # calculate the mean of parameter distribution
    np.array(accepted_samples)
    mean_params = np.mean(accepted_samples, axis=0)

    print('Finished guessing')
    print(f'best-fit parameters: {mean_params}')

    # return the best-fit params
    return mean_params


# pylint: disable=R1710
# pylint: disable=W1518
# noinspection PyUnresolvedReferences
class CurveFitMixin:
    """A mixin class providing curve fitting capabilities

    Attributes
    ----------
    initial_guess:
        The

    """

    @property
    @cache
    def _caption_text(self):
        """Generate caption from the doctring of model"""

        # get model name and parameter name from the doctring of our model
        model_name, param_name = self.model.__doc__.split('Params:')

        # strip white spaces
        model_name = model_name.strip()
        param_name = param_name.strip().split(',')

        param_name = [s.strip() for s in param_name]

        # combine parameter value with error
        param_values = [fr'{value: .2f} \pm {error: .2f} ' for value, error
                        in zip(self.best_fit_params, self.err_params)]

        # combine parameter value with name
        param_name_final = r'\hspace{12pt}'.join([fr'\( {name} = {value} \) ' for name, value in
                                                  zip(param_name, param_values)])
        if self.reduced_chi_squared is not None:
            # add some space between model name and parameter value
            text = '\n \n'.join([model_name, param_name_final, r'\( \chi^2_{reduced} = \) '
                                                               fr'{self.reduced_chi_squared: .3f}'])
        else:
            text = '\n \n'.join([model_name, param_name_final])

        return text

    @cached_property
    def initial_guess(self):
        """The initial guess on the best-fit parameters.

        If not provided, Metropolis algorithm will be used to provide and initial estimate
        """

        return mh(self.model, self.x, self.y)

    @property
    @cache
    def _fit_result(self):
        """An array containing the best-fit parameters and covariant matrix"""

        # check if curve fitting is required
        if self.model is None:
            raise ValueError('Please provide fitting model')

        return curve_fit(self.model, self.x, self.y,
                         sigma=self.err_y, p0=self.initial_guess)

    @property
    @cache
    def best_fit_params(self):
        """An array of best-fit parameters"""
        return self._fit_result[0]

    @property
    @cache
    def err_params(self):
        """An array of errors on best-fit parameters"""

        cov = self._fit_result[1]  # get covariant matrix

        return np.sqrt(np.diag(cov))

    @property
    @cache
    def reduced_chi_squared(self):
        """The reduced chi-squared value"""

        # check if this is a chi-squared regression
        if self.err_y is not None:
            # calculate degrees of freedom
            number_of_data = self._df.shape[0]
            number_of_parameters = len(self.best_fit_params)
            degrees_of_freedom = number_of_data - number_of_parameters

            # calculate chi-squared
            chi_squared = sum(((self.y_predict - self.y) / self.err_y) ** 2)

            # calculate reduced chi-squared
            return chi_squared / degrees_of_freedom

    @property
    @cache
    def y_predict(self):
        """Predicted y values given the best fit parameters"""

        # check if curve fitting is required
        if self.model is not None:
            return self.model(self.x, *self.best_fit_params)
