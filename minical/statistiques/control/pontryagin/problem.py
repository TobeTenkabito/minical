class PMPProblem:
    def __init__(self, dynamics, running_cost, terminal_cost, x0, T):
        self.f = dynamics
        self.L = running_cost
        self.g = terminal_cost
        self.x0 = x0
        self.T = T
