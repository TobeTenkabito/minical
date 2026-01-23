import math
from .core import Expr, register_op


@register_op("const")
class Const(Expr):
    def __init__(self, value):
        self.value = float(value)

    def eval(self, env):
        return self.value

    def diff(self, var):
        return Const(0.0)

    def __repr__(self):
        return f"{self.value}"


@register_op("var")
class Var(Expr):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

    def diff(self, var):
        return Const(1.0 if self.name == var else 0.0)

    def __repr__(self):
        return self.name


@register_op("add")
class Add(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, env):
        return self.a.eval(env) + self.b.eval(env)

    def diff(self, var):
        return Add(self.a.diff(var), self.b.diff(var))

    def __repr__(self):
        return f"({self.a} + {self.b})"


@register_op("mul")
class Mul(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, env):
        return self.a.eval(env) * self.b.eval(env)

    def diff(self, var):
        return Add(
            Mul(self.a.diff(var), self.b),
            Mul(self.a, self.b.diff(var))
        )

    def __repr__(self):
        return f"({self.a} * {self.b})"


@register_op("neg")
class Neg(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return -self.x.eval(env)

    def diff(self, var):
        return Neg(self.x.diff(var))

    def __repr__(self):
        return f"(-{self.x})"


@register_op("sin")
class Sin(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.sin(self.x.eval(env))

    def diff(self, var):
        return Mul(Cos(self.x), self.x.diff(var))

    def __repr__(self):
        return f"sin({self.x})"


@register_op("cos")
class Cos(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.cos(self.x.eval(env))

    def diff(self, var):
        return Neg(Mul(Sin(self.x), self.x.diff(var)))

    def __repr__(self):
        return f"cos({self.x})"


@register_op("tan")
class Tan(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.tan(self.x.eval(env))

    def diff(self, var):
        return Mul(
            Pow(Cos(self.x), Const(-2.0)),
            self.x.diff(var)
        )

    def __repr__(self):
        return f"tan({self.x})"


@register_op("exp")
class Exp(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.exp(self.x.eval(env))

    def diff(self, var):
        return Mul(self, self.x.diff(var))

    def __repr__(self):
        return f"exp({self.x})"


@register_op("log")
class Log(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.log(self.x.eval(env))

    def diff(self, var):
        return Mul(
            Pow(self.x, Const(-1.0)),
            self.x.diff(var)
        )

    def __repr__(self):
        return f"log({self.x})"


@register_op("sqrt")
class Sqrt(Expr):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return math.sqrt(self.x.eval(env))

    def diff(self, var):
        return Mul(
            Mul(Const(0.5), Pow(self.x, Const(-0.5))),
            self.x.diff(var)
        )

    def __repr__(self):
        return f"sqrt({self.x})"


@register_op("pow")
class Pow(Expr):
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp

    def eval(self, env):
        return self.base.eval(env) ** self.exp.eval(env)

    def diff(self, var):
        if not isinstance(self.exp, Const):
            raise NotImplementedError("pow diff only supports constant exponent")

        return Mul(
            Mul(self.exp, Pow(self.base, Const(self.exp.value - 1))),
            self.base.diff(var)
        )

    def __repr__(self):
        return f"({self.base} ** {self.exp})"
