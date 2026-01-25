class PMPSolver:
    def __init__(self, problem, policy, dt=0.01):
        self.p = problem
        self.policy = policy
        self.dt = dt

    def solve(self, lam_T):
        # forward-backward integration
        x = self.p.x0
        lam = lam_T
        t = self.p.T

        # backward λ
        while t > 0:
            u = self.policy(x, lam, t)
            lam -= self.dt * self._adjoint(x, lam, u, t)
            t -= self.dt

        return lam  # shooting residual
