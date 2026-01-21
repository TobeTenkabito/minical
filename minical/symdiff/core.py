
class Expr:
    def diff(self, var): raise NotImplementedError

    def simplify(self): return self

    def subs(self, mapping): raise NotImplementedError

    def eval(self): raise NotImplementedError

    def __add__(self, other):
        from .ops import Add
        return Add(self, ensure_expr(other))

    def __sub__(self, other):
        from .ops import Add, Mul
        return Add(self, Mul(Const(-1), ensure_expr(other)))

    def __mul__(self, other):
        from .ops import Mul
        return Mul(self, ensure_expr(other))

    def __truediv__(self, other):
        from .ops import Div
        return Div(self, ensure_expr(other))

    def __pow__(self, other):
        from .ops import Pow
        return Pow(self, ensure_expr(other))

    def __str__(self): raise NotImplementedError


class Const(Expr):
    def __init__(self, value): self.value = value
    def diff(self, var): return Const(0)
    def subs(self, mapping): return self
    def eval(self): return self.value
    def __str__(self): return str(self.value)
    def __int__(self): return int(self.value)
    def __float__(self): return float(self.value)


class Var(Expr):
    def __init__(self, name): self.name = name
    def diff(self, var): return Const(1) if self.name == var else Const(0)

    def subs(self, mapping):
        if self.name in mapping:
            return ensure_expr(mapping[self.name])
        return self

    def eval(self): raise ValueError("Unbound variable")
    def __str__(self): return self.name


def ensure_expr(x):
    return x if isinstance(x, Expr) else Const(x)


def vars(names: str):
    return tuple(Var(n) for n in names.split())
