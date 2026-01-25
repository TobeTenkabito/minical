import math
import random
from .core import RV, Const


class Distribution(RV):
    def mean(self):
        raise NotImplementedError

    def sample(self, n=1):
        raise NotImplementedError


class Normal(Distribution):
    def __init__(self, mu, sigma):
        self.mu = mu if isinstance(mu, RV) else Const(mu)
        self.sigma = sigma if isinstance(sigma, RV) else Const(sigma)

    def mean(self):
        return self.mu

    def sample(self, n=1):
        from .sampling import _sample_once

        samples = []
        for _ in range(n):
            mu = _sample_once(self.mu)
            sigma = _sample_once(self.sigma)
            samples.append(random.gauss(mu, sigma))
        return samples

    def __repr__(self):
        return f"Normal({self.mu}, {self.sigma})"


class Uniform(Distribution):
    def __init__(self, a, b):
        self.a = a if isinstance(a, RV) else Const(a)
        self.b = b if isinstance(b, RV) else Const(b)

    def mean(self):
        return (self.a + self.b) / 2

    def sample(self, n=1):
        a = float(self.a.value)
        b = float(self.b.value)
        return [random.uniform(a, b) for _ in range(n)]

    def __repr__(self):
        return f"Uniform({self.a}, {self.b})"
