import math
import random

from .core import Const, Symbol
from .ops import Add, Sub, Mul, Div, Neg, Pow
from .funcs import Sin, Cos, Exp, Log, Abs
from .distributions import Distribution


def sample(expr, n=1, seed=None):
    if seed is not None:
        random.seed(seed)
    return [_sample_once(expr) for _ in range(n)]


def _sample_once(expr):
    # Constant
    if isinstance(expr, Const):
        return float(expr.value)

    # Distribution
    if isinstance(expr, Distribution):
        return expr.sample(1)[0]

    # Free symbol
    if isinstance(expr, Symbol):
        raise ValueError(f"Cannot sample free symbol: {expr}")

    # Unary minus
    if isinstance(expr, Neg):
        return -_sample_once(expr.a)

    # Binary ops
    if isinstance(expr, Add):
        return _sample_once(expr.a) + _sample_once(expr.b)

    if isinstance(expr, Sub):
        return _sample_once(expr.a) - _sample_once(expr.b)

    if isinstance(expr, Mul):
        return _sample_once(expr.a) * _sample_once(expr.b)

    if isinstance(expr, Div):
        return _sample_once(expr.a) / _sample_once(expr.b)

    if isinstance(expr, Pow):
        return _sample_once(expr.a) ** _sample_once(expr.b)

    # Elementary functions (unary)
    if isinstance(expr, Sin):
        return math.sin(_sample_once(expr.a))

    if isinstance(expr, Cos):
        return math.cos(_sample_once(expr.a))

    if isinstance(expr, Exp):
        return math.exp(_sample_once(expr.a))

    if isinstance(expr, Log):
        return math.log(_sample_once(expr.a))

    if isinstance(expr, Abs):
        return abs(_sample_once(expr.a))

    raise TypeError(f"Unsupported expression type: {type(expr)}")
