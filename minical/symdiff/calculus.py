from .core import Var


def diff(expr, var):
    if isinstance(var, str):
        var = Var(var)
    return expr.diff(var.name).simplify()
