from .sampling import sample


def posterior_predictive(expr, n=1000):
    return sample(expr, n)
