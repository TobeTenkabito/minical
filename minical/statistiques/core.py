class RV:
    def __add__(self, other):
        from .ops import Add
        return Add(self, other)

    def __radd__(self, other):
        from .ops import Add
        return Add(other, self)

    def __sub__(self, other):
        from .ops import Sub
        return Sub(self, other)

    def __rsub__(self, other):
        from .ops import Sub
        return Sub(other, self)

    def __mul__(self, other):
        from .ops import Mul
        return Mul(self, other)

    def __rmul__(self, other):
        from .ops import Mul
        return Mul(other, self)

    def __truediv__(self, other):
        from .ops import Div
        return Div(self, other)

    def __neg__(self):
        from .ops import Neg
        return Neg(self)

    def __pow__(self, other):
        from .ops import Pow
        return Pow(self, other)


class Symbol(RV):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Const(RV):
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return str(self.value)
