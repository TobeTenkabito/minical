from .variance import var
from .covariance import cov
from .core import Const
from .funcs import exp
from .ops import Pow


def corr(x, y):
    vx = var(x)
    vy = var(y)
    return cov(x, y) / (vx * vy) ** Const(0.5)
