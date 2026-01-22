from .core import Add, Mul, Transpose, Inverse, Expr, Const, ScalarMul, Scalar, ScalarAdd, Func


def add(a: Expr, b: Expr) -> Expr:
    if isinstance(a, Const) and a.name == "0":
        return b
    if isinstance(b, Const) and b.name == "0":
        return a
    if isinstance(a, Scalar) and isinstance(b, Scalar):
        return Scalar(f"({a.name} + {b.name})")
    if isinstance(a, Scalar) and not isinstance(b, Scalar):
        return ScalarAdd(a, b)
    if isinstance(b, Scalar) and not isinstance(a, Scalar):
        return ScalarAdd(b, a)
    return Add(a, b)


def mul(a: Expr, b: Expr) -> Expr:
    if isinstance(a, Scalar) and not isinstance(b, Scalar):
        return ScalarMul(a, b)
    if isinstance(b, Scalar) and not isinstance(a, Scalar):
        return ScalarMul(b, a)
    if isinstance(a, Const) and a.name == "I":
        return b
    if isinstance(b, Const) and b.name == "I":
        return a
    if isinstance(a, Const) and a.name == "0":
        return a
    if isinstance(b, Const) and b.name == "0":
        return b
    return Mul(a, b)


def transpose(x: Expr) -> Expr:
    if isinstance(x, Transpose):
        return x.x
    return Transpose(x)


def inverse(x: Expr) -> Expr:
    if isinstance(x, Inverse):
        return x.x
    return Inverse(x)


def func(name: str, *args: Expr) -> Expr:
    return Func(name, args)