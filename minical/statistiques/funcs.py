from .core import RV, Const
from .ops import UnaryOp


def _wrap(x):
    if isinstance(x, RV):
        return x
    return Const(x)


class Func(UnaryOp):
    name = "func"

    def __repr__(self):
        return f"{self.name}({self.a})"


class Sin(Func):
    name = "sin"


class Cos(Func):
    name = "cos"


class Exp(Func):
    name = "exp"


class Log(Func):
    name = "log"


class Abs(Func):
    name = "abs"

class Pow(Func):
    name = "pow"


def sin(x):
    return Sin(_wrap(x))


def cos(x):
    return Cos(_wrap(x))


def exp(x):
    return Exp(_wrap(x))


def log(x):
    return Log(_wrap(x))


def abs(x):
    return Abs(_wrap(x))

def pow(x):
    return Pow(_wrap(x))
