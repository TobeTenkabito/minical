class StochasticProcess:

    def __init__(self, x0):
        self.x0 = x0

    def step(self, x, t):
        raise NotImplementedError

    def simulate(self, n_steps, n_samples=1000):
        from .sampling import sample

        paths = []

        for _ in range(n_samples):
            x = self.x0
            path = [x]

            for t in range(n_steps):
                x = self.step(x, t)
                x = sample(x, 1)[0]
                path.append(x)

            paths.append(path)

        return paths

