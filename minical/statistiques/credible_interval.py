from .posterior_predictive import posterior_predictive


def credible_interval(expr, level=0.95, n=10000):
    """
    Bayesian credible interval via posterior predictive sampling.

    expr: RV
        Posterior predictive expression
    level: float
        Credible mass, e.g. 0.95
    n: int
        Number of samples
    """
    if not (0 < level < 1):
        raise ValueError("level must be in (0, 1)")

    samples = posterior_predictive(expr, n)
    samples = sorted(samples)

    alpha = 1.0 - level
    lo_idx = int(alpha / 2 * n)
    hi_idx = int((1 - alpha / 2) * n)

    return samples[lo_idx], samples[hi_idx]


def predictive_summary(expr, level=0.95, n=10000):
    """
    Return (mean, (lo, hi)) for posterior predictive.
    """
    samples = posterior_predictive(expr, n)
    samples_sorted = sorted(samples)

    mean = sum(samples) / len(samples)

    alpha = 1.0 - level
    lo = samples_sorted[int(alpha / 2 * n)]
    hi = samples_sorted[int((1 - alpha / 2) * n)]

    return mean, (lo, hi)
