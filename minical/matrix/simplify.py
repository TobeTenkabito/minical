from .core import Expr, Add, Transpose, Inverse, Const, Mul, Func
from .ops import add, mul


def simplify(expr: Expr) -> Expr:
    if isinstance(expr, Add):
        a = simplify(expr.a)
        b = simplify(expr.b)
        return add(a, b)

    if isinstance(expr, Mul):
        a = simplify(expr.a)
        b = simplify(expr.b)
        if isinstance(b, Const) and b.name == "I":
            return a
        if isinstance(a, Const) and a.name == "I":
            return b
        return mul(a, b)

    if isinstance(expr, Transpose):
        x = simplify(expr.x)
        if isinstance(x, Transpose):
            return x.x
        return Transpose(x)

    if isinstance(expr, Inverse):
        x = simplify(expr.x)
        if isinstance(x, Inverse):
            return x.x
        return Inverse(x)

    if isinstance(expr, Func):
        args = tuple(simplify(a) for a in expr.args)
        if expr.name == "exp" and len(args) == 1:
            arg = args[0]
            if isinstance(arg, Func) and arg.name == "log" and len(arg.args) == 1:
                return simplify(arg.args[0])
        if expr.name == "log" and len(args) == 1:
            arg = args[0]
            if isinstance(arg, Func) and arg.name == "exp" and len(arg.args) == 1:
                return simplify(arg.args[0])
        if expr.name == "exp" and len(args) == 1:
            arg = args[0]
            if isinstance(arg, Func) and arg.name == "ln":
                return simplify(arg.args[0])
        if expr.name == "ln" and len(args) == 1:
            arg = args[0]
            if isinstance(arg, Func) and arg.name == "exp":
                return simplify(arg.args[0])
        if expr.name == "pow" and len(args) == 2:
            base, exponent = args
            if isinstance(exponent, Const) and exponent.name == "1":
                return base
            if isinstance(exponent, Const) and exponent.name == "0":
                return Const("1", (1,1))
        return Func(expr.name, args)

    return expr
