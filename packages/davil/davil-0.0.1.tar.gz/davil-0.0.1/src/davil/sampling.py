import numpy as np


def sample_index_multinominal(probs):
    if sum(probs) != 1:
        raise ValueError('Specified probabilities must sum to 1.')
    one_hot = np.random.multinomial(1, probs)
    return np.argmax(one_hot)


def sample_bernoulli(prob):
    return np.random.binomial(1, prob)


def sample_continuous_range(lower, upper):
    if upper < lower:
        raise ValueError('Upper bound must be smaller than lower bound.')
    return ((upper - lower) * np.random.random()) + lower
