import inspect
import numpy as np


def mh(model, x, y_actual, sigma=1):
    """
    Metropolis-Hasting algorithm

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
