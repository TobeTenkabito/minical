from .core import Const
from .expectation import E


def var(expr):
    mu = E(expr)
    return E((expr - mu) ** Const(2))
