class PMPPolicy:
    def __init__(self, u_star):
        self.u_star = u_star  # u*(x, λ, t)

    def __call__(self, x, lam, t):
        return self.u_star(x, lam, t)
