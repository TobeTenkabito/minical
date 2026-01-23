from .core import make_op, Expr


def _ensure_expr(x):
    if isinstance(x, Expr):
        return x
    return make_op("const", x)


def sin(x):
    return make_op("sin", _ensure_expr(x))


def cos(x):
    return make_op("cos", _ensure_expr(x))


def tan(x):
    return make_op("tan", _ensure_expr(x))


def exp(x):
    return make_op("exp", _ensure_expr(x))


def log(x):
    return make_op("log", _ensure_expr(x))


def sqrt(x):
    return make_op("sqrt", _ensure_expr(x))


def pow(x, y):
    return make_op("pow", _ensure_expr(x), _ensure_expr(y))
