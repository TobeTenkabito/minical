from ..core import Const
from ..distributions import Normal


def bayes_linear_1d(prior, x, y, sigma):
    """
    Bayesian linear regression (1D):
        y = w * x + eps
        eps ~ N(0, sigma^2)
        w ~ Normal(mu0, s0)

    Parameters
    ----------
    prior : Normal
        Prior on w
    x : list of float
        Inputs
    y : list of float
        Observations
    sigma : float or Const
        Noise std

    Returns
    -------
    Normal
        Posterior over w
    """
    if not isinstance(prior, Normal):
        raise TypeError("prior must be Normal")

    if len(x) != len(y):
        raise ValueError("x and y must have same length")

    mu0 = prior.mu
    s0 = prior.sigma

    sigma = sigma if isinstance(sigma, Const) else Const(sigma)

    sum_x2 = Const(0)
    sum_xy = Const(0)

    for xi, yi in zip(x, y):
        xi = xi if isinstance(xi, Const) else Const(xi)
        yi = yi if isinstance(yi, Const) else Const(yi)
        sum_x2 = sum_x2 + xi * xi
        sum_xy = sum_xy + xi * yi

    # posterior variance
    var_n = Const(1) / (
        Const(1) / (s0 ** Const(2)) +
        sum_x2 / (sigma ** Const(2))
    )

    # posterior mean
    mu_n = var_n * (
        mu0 / (s0 ** Const(2)) +
        sum_xy / (sigma ** Const(2))
    )

    return Normal(mu_n, var_n ** Const(0.5))
