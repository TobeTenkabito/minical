"""
Path functionals for stochastic processes.

All functions take:
    paths: List[List[float]]

and return:
    - List[float]          (scalar functional)
    - List[List[float]]    (path-valued functional)
"""


def max_value(paths):
    return [max(path) for path in paths]


def min_value(paths):
    return [min(path) for path in paths]


def terminal_value(paths):
    return [path[-1] for path in paths]


def running_mean(paths):
    results = []

    for path in paths:
        acc = 0.0
        rm = []
        for i, x in enumerate(path, start=1):
            acc += x
            rm.append(acc / i)
        results.append(rm)

    return results


def hitting_time(paths, level):
    """
    First hitting time of a given level.
    Returns a list of indices (or None if never hit).
    """
    times = []

    for path in paths:
        hit = None
        for i, x in enumerate(path):
            if x >= level:
                hit = i
                break
        times.append(hit)

    return times
