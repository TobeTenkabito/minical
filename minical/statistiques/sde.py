from .distributions import Normal
from .sampling import sample


def _is_vector(x):
    return isinstance(x, (list, tuple))


def _add(x, dx):
    if _is_vector(x):
        return [a + b for a, b in zip(x, dx)]
    return x + dx


class SDE:
    def __init__(
        self,
        drift,
        diffusion,
        x0,
        dt=0.01,
        method="euler",
        noise=None,
        diffusion_dx=None,
    ):
        self.drift = drift
        self.diffusion = diffusion
        self.x0 = x0
        self.dt = dt
        self.method = method
        self.noise = noise or self._default_noise
        self.diffusion_dx = diffusion_dx

    def _default_noise(self, sigma):
        return Normal(0, sigma)

    def step(self, x, t):
        if self.method == "euler":
            return self._step_euler(x, t)
        elif self.method == "milstein":
            return self._step_milstein(x, t)
        else:
            raise ValueError(f"Unknown SDE method: {self.method}")

    def _step_euler(self, x, t):
        dt = self.dt
        mu = self.drift(x, t)
        sigma = self.diffusion(x, t)

        if _is_vector(x):
            dx = []
            for m, s in zip(mu, sigma):
                rv = self.noise(s * dt ** 0.5)
                eps = sample(rv, 1)[0]
                dx.append(m * dt + eps)
            return _add(x, dx)

        rv = self.noise(sigma * dt ** 0.5)
        eps = sample(rv, 1)[0]
        return x + mu * dt + eps

    def _step_milstein(self, x, t):
        if self.diffusion_dx is None:
            raise ValueError("Milstein method requires diffusion_dx")

        dt = self.dt
        mu = self.drift(x, t)
        sigma = self.diffusion(x, t)
        dsigma = self.diffusion_dx(x, t)

        rv = self.noise(sigma * dt ** 0.5)
        dW = sample(rv, 1)[0]

        correction = 0.5 * sigma * dsigma * (dW * dW - dt)

        return x + mu * dt + dW + correction

    def simulate(self, T, n_samples=1000):
        n_steps = int(T / self.dt)
        paths = []

        for _ in range(n_samples):
            x = self.x0
            path = [x]

            for i in range(n_steps):
                t = i * self.dt
                x = self.step(x, t)
                path.append(x)

            paths.append(path)

        return paths
