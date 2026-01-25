class AdjointSystem:
    def __init__(self, problem, control):
        self.p = problem
        self.control = control

    def forward(self, x, t):
        u = self.control(x, t)
        return self.p.f(x, u, t)

    def backward(self, x, lam, u, t):
        # -∂H/∂x
        eps = 1e-6
        fx = (self.p.f(x + eps, u, t) - self.p.f(x - eps, u, t)) / (2 * eps)
        Lx = (self.p.L(x + eps, u, t) - self.p.L(x - eps, u, t)) / (2 * eps)
        return -(Lx + lam * fx)
