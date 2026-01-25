from .process import StochasticProcess
from .distributions import Normal


class AR1(StochasticProcess):
    def __init__(self, phi, sigma, x0):
        super().__init__(x0)
        self.phi = phi
        self.sigma = sigma

    def step(self, x, t):
        return self.phi * x + Normal(0, self.sigma)


class RandomWalk(StochasticProcess):
    def __init__(self, sigma, x0=0.0):
        super().__init__(x0)
        self.sigma = sigma

    def step(self, x, t):
        from .distributions import Normal
        return x + Normal(0, self.sigma)