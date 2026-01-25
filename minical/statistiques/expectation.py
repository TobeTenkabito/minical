from .core import RV, Const
from .ops import Add, Sub, Mul, Div, Neg
from .funcs import Func
from .distributions import Distribution


def E(expr):
    if isinstance(expr, Const):
        return expr
    if isinstance(expr, Distribution):
        return expr.mean()
    if isinstance(expr, Add):
        return E(expr.a) + E(expr.b)

    if isinstance(expr, Sub):
        return E(expr.a) - E(expr.b)

    if isinstance(expr, Neg):
        return -E(expr.a)

    if isinstance(expr, Mul):
        if isinstance(expr.a, Const):
            return expr.a * E(expr.b)
        if isinstance(expr.b, Const):
            return expr.b * E(expr.a)
        return expr

    if isinstance(expr, Div):
        if isinstance(expr.b, Const):
            return E(expr.a) / expr.b
        return expr
    if isinstance(expr, Func):
        return expr
    if isinstance(expr, RV):
        return expr

    raise TypeError(f"Unsupported expression type: {type(expr)}")
