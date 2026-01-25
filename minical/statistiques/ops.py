from .core import RV, Const


def _wrap(x):
    if isinstance(x, RV):
        return x
    return Const(x)


class Op(RV):
    pass


class UnaryOp(Op):
    def __init__(self, a):
        self.a = _wrap(a)


class BinaryOp(Op):
    def __init__(self, a, b):
        self.a = _wrap(a)
        self.b = _wrap(b)


class Add(BinaryOp):
    def __repr__(self):
        return f"({self.a} + {self.b})"


class Sub(BinaryOp):
    def __repr__(self):
        return f"({self.a} - {self.b})"


class Mul(BinaryOp):
    def __repr__(self):
        return f"({self.a} * {self.b})"


class Div(BinaryOp):
    def __repr__(self):
        return f"({self.a} / {self.b})"


class Neg(UnaryOp):
    def __repr__(self):
        return f"(-{self.a})"


class Pow(RV):
    def __init__(self, a, b):
        self.a = a if isinstance(a, RV) else Const(a)
        self.b = b if isinstance(b, RV) else Const(b)

    def __repr__(self):
        return f"({self.a} ** {self.b})"
