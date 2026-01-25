from .core import RV
from .expectation import E


def cov(x, y):
    mx = E(x)
    my = E(y)
    return E((x - mx) * (y - my))
