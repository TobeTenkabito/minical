from .core import Posterior
from ..distributions import Normal
from ..core import Const


def normal_normal(prior, data, sigma):
    if not isinstance(prior, Normal):
        raise TypeError("prior must be Normal")

    mu0 = prior.mu
    s0 = prior.sigma

    n = Const(len(data))
    sum_y = Const(0)

    for y in data:
        sum_y = sum_y + (y if isinstance(y, Const) else Const(y))

    sigma = sigma if isinstance(sigma, Const) else Const(sigma)

    # σ_n^2
    var_n = Const(1) / (Const(1) / (s0 ** Const(2)) + n / (sigma ** Const(2)))

    # μ_n
    mu_n = var_n * (
        mu0 / (s0 ** Const(2)) + sum_y / (sigma ** Const(2))
    )

    return Normal(mu_n, var_n ** Const(0.5))
