import math


class HJBProblem:
    def __init__(
        self,
        drift,          # b(x, u)
        diffusion,      # sigma(x, u)
        reward,         # r(x, u)
        controls,       # iterable of u
        x_grid,         # list[float]
        t_grid,         # list[float] (forward time, internally backward)
        terminal        # g(x)
    ):
        self.drift = drift
        self.diffusion = diffusion
        self.reward = reward
        self.controls = list(controls)

        self.x = list(x_grid)
        self.t = list(t_grid)

        self.dx = self.x[1] - self.x[0]
        self.dt = self.t[1] - self.t[0]

        self.Nx = len(self.x)
        self.Nt = len(self.t)
        self.V = [
            [0.0 for _ in range(self.Nx)]
            for _ in range(self.Nt)
        ]
        for i, xi in enumerate(self.x):
            self.V[-1][i] = terminal(xi)

    def _dx(self, V, i):
        return (V[i + 1] - V[i - 1]) / (2 * self.dx)

    def _dxx(self, V, i):
        return (V[i + 1] - 2 * V[i] + V[i - 1]) / (self.dx ** 2)

    def _bellman(self, V_next, i):
        x = self.x[i]
        best = -1e300

        Vx = self._dx(V_next, i)
        Vxx = self._dxx(V_next, i)

        for u in self.controls:
            b = self.drift(x, u)
            s = self.diffusion(x, u)
            r = self.reward(x, u)

            val = r + b * Vx + 0.5 * s * s * Vxx

            if val > best:
                best = val

        return best

    def step(self, n):
        V_next = self.V[n + 1]
        V_now = self.V[n]
        V_now[0] = V_next[0]
        V_now[-1] = V_next[-1]

        for i in range(1, self.Nx - 1):
            H = self._bellman(V_next, i)
            V_now[i] = V_next[i] + self.dt * H

    def solve(self):
        for n in range(self.Nt - 2, -1, -1):
            self.step(n)
        return self.V

    def optimal_control(self, t_index, x_index):
        V_next = self.V[t_index + 1]
        x = self.x[x_index]

        Vx = self._dx(V_next, x_index)
        Vxx = self._dxx(V_next, x_index)

        best_u = None
        best_val = -1e300

        for u in self.controls:
            val = (
                self.reward(x, u)
                + self.drift(x, u) * Vx
                + 0.5 * self.diffusion(x, u) ** 2 * Vxx
            )
            if val > best_val:
                best_val = val
                best_u = u

        return best_u
