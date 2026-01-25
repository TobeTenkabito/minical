from .sampling import sample


def simulate(step_expr, x0, n_steps, n_samples=1000):
    """
    Bayesian time series simulation.

    step_expr: function(x) -> RV
        State transition expression
    x0: RV or number
        Initial state
    n_steps: int
        Number of time steps
    n_samples: int
        Monte Carlo samples
    """
    trajectories = []

    for _ in range(n_samples):
        x = x0
        path = [x]

        for _ in range(n_steps):
            x = step_expr(x)
            x = sample(x, 1)[0]
            path.append(x)

        trajectories.append(path)

    return trajectories
