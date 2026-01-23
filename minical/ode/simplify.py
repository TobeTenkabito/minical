from .core import Expr
from .ops import (
    Const, Var,
    Add, Mul, Neg,
    Pow
)


def simplify(expr: Expr) -> Expr:
    if isinstance(expr, (Const, Var)):
        return expr
    if isinstance(expr, Neg):
        x = simplify(expr.x)
        if isinstance(x, Const):
            return Const(-x.value)

        return Neg(x)
    if isinstance(expr, Add):
        a = simplify(expr.a)
        b = simplify(expr.b)
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.value + b.value)
        if isinstance(b, Const) and b.value == 0.0:
            return a
        if isinstance(a, Const) and a.value == 0.0:
            return b

        return Add(a, b)
    if isinstance(expr, Mul):
        a = simplify(expr.a)
        b = simplify(expr.b)
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.value * b.value)
        if (isinstance(a, Const) and a.value == 0.0) or \
           (isinstance(b, Const) and b.value == 0.0):
            return Const(0.0)
        if isinstance(a, Const) and a.value == 1.0:
            return b
        if isinstance(b, Const) and b.value == 1.0:
            return a

        return Mul(a, b)
    if isinstance(expr, Pow):
        base = simplify(expr.base)
        exp = simplify(expr.exp)
        if isinstance(exp, Const) and exp.value == 1.0:
            return base
        if isinstance(exp, Const) and exp.value == 0.0:
            return Const(1.0)
        if isinstance(base, Const) and isinstance(exp, Const):
            return Const(base.value ** exp.value)

        return Pow(base, exp)
    return expr
