from .core import ensure_expr, Const
from .ops import (
    Sin, Cos, Tan, Exp, Ln, Asin, Acos, Atan,
    Sinh, Cosh, Tanh, ExpBase, LogBase, Pow
)
import math


def sin(x):
    return Sin(ensure_expr(x))


def cos(x):
    return Cos(ensure_expr(x))


def tan(x):
    return Tan(ensure_expr(x))


def asin(x):
    return Asin(ensure_expr(x))


def acos(x):
    return Acos(ensure_expr(x))


def atan(x):
    return Atan(ensure_expr(x))


def sinh(x):
    return Sinh(ensure_expr(x))


def cosh(x):
    return Cosh(ensure_expr(x))


def tanh(x):
    return Tanh(ensure_expr(x))


def exp(x):
    """ e^x """
    return Exp(ensure_expr(x))


def ln(x):
    return Ln(ensure_expr(x))

def log(x):
    return LogBase(Const(10), ensure_expr(x))


def expbase(base, x):
    return ExpBase(ensure_expr(base), ensure_expr(x))


def logbase(base, x):
    return LogBase(ensure_expr(base), ensure_expr(x))


def sqrt(x):
    return Pow(ensure_expr(x), Const(0.5))


def E():
    return Const(math.e)


def PI():
    return Const(math.pi)