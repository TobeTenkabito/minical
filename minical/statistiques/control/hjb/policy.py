def _find_index(grid, value):
    """
    Return i such that grid[i] <= value <= grid[i+1]
    Clamp to boundary if outside.
    """
    if value <= grid[0]:
        return 0
    if value >= grid[-2]:
        return len(grid) - 2

    for i in range(len(grid) - 1):
        if grid[i] <= value <= grid[i + 1]:
            return i
    return len(grid) - 2


class Policy:
    def __call__(self, x, t):
        raise NotImplementedError


class HJBPolicy(Policy):
    """
    Feedback policy derived from solved HJBProblem.
    """

    def __init__(self, hjb_problem):
        self.hjb = hjb_problem
        self.x_grid = hjb_problem.x
        self.t_grid = hjb_problem.t

    def _time_index(self, t):
        if t <= self.t_grid[0]:
            return 0
        if t >= self.t_grid[-2]:
            return len(self.t_grid) - 2
        return _find_index(self.t_grid, t)

    def _space_index(self, x):
        return _find_index(self.x_grid, x)

    def __call__(self, x, t):
        ti = self._time_index(t)
        xi = self._space_index(x)
        return self.hjb.optimal_control(ti, xi)


class InterpolatedHJBPolicy(HJBPolicy):
    """
    Linear interpolation in time for smoother control.
    """

    def __call__(self, x, t):
        ti = self._time_index(t)
        xi = self._space_index(x)

        t0 = self.t_grid[ti]
        t1 = self.t_grid[ti + 1]
        w = (t - t0) / (t1 - t0) if t1 > t0 else 0.0

        u0 = self.hjb.optimal_control(ti, xi)
        u1 = self.hjb.optimal_control(ti + 1, xi)

        return (1 - w) * u0 + w * u1
