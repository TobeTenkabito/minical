from .core import Expr, Const, ensure_expr
import math


class Add(Expr):
    def __init__(self, a, b):
        self.a = ensure_expr(a)
        self.b = ensure_expr(b)

    def diff(self, var): return Add(self.a.diff(var), self.b.diff(var))

    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.value == 0: return b
        if isinstance(b, Const) and b.value == 0: return a
        if isinstance(a, Const) and isinstance(b, Const): return Const(a.value + b.value)
        return Add(a, b)

    def subs(self, mapping): return Add(self.a.subs(mapping), self.b.subs(mapping))
    def eval(self): return self.a.eval() + self.b.eval()

    def __str__(self):
        return f"({self.a} + {self.b})"


class Sub(Expr):
    def __init__(self, a, b):
        self.a = ensure_expr(a)
        self.b = ensure_expr(b)

    def diff(self, var): return Sub(self.a.diff(var), self.b.diff(var))

    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.value == 0: return b
        if isinstance(b, Const) and b.value == 0: return a
        if isinstance(a, Const) and isinstance(b, Const): return Const(a.value - b.value)
        return Sub(a, b)

    def subs(self, mapping): return Sub(self.a.subs(mapping), self.b.subs(mapping))
    def eval(self): return self.a.eval() - self.b.eval()

    def __str__(self):
        return f"({self.a} - {self.b})"


class Mul(Expr):
    def __init__(self, a, b):
        self.a = ensure_expr(a)
        self.b = ensure_expr(b)

    def diff(self, var): return Add(Mul(self.a.diff(var), self.b), Mul(self.a, self.b.diff(var)))

    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.value == 0:
            return Const(0)
        if isinstance(b, Const) and b.value == 0:
            return Const(0)
        if isinstance(a, Const) and a.value == 1:
            return b
        if isinstance(b, Const) and b.value == 1:
            return a
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.value * b.value)

        return Mul(a, b)

    def subs(self, mapping): return Mul(self.a.subs(mapping), self.b.subs(mapping))

    def eval(self): return self.a.eval() * self.b.eval()

    def __str__(self):
        return f"({self.a} * {self.b})"


class Div(Expr):
    def __init__(self, num, den):
        self.num = ensure_expr(num)
        self.den = ensure_expr(den)

    def diff(self, var):
        return Div(
            Add(Mul(self.num.diff(var), self.den), Mul(Const(-1), Mul(self.num, self.den.diff(var)))),
            Pow(self.den, 2))

    def simplify(self):
        num = self.num.simplify()
        den = self.den.simplify()
        if isinstance(num, Const) and num.value == 0:return Const(0)
        if isinstance(den, Const) and den.value == 1:return num
        if isinstance(num, Const) and isinstance(den, Const):return Const(num.value / den.value)
        return Div(num, den)

    def subs(self, mapping): return Div(self.num.subs(mapping), self.den.subs(mapping))

    def eval(self):
        den = self.den.eval()
        if den == 0:
            raise ZeroDivisionError("Division by zero")
        return self.num.eval() / den

    def __str__(self):
        return f"({self.num} / {self.den})"


class Pow(Expr):
    def __init__(self, base, power):
        self.base = ensure_expr(base)
        self.power = ensure_expr(power)

    def diff(self, var):
        if isinstance(self.power, (int, float, Const)):
            p = self.power.value if isinstance(self.power, Const) else self.power
            return Mul(Mul(Const(p), Pow(self.base, p - 1)), self.base.diff(var))
        return Mul(
            Pow(self.base, self.power),
            Add(Mul(self.power.diff(var), Ln(self.base)), Mul(self.power, Div(self.base.diff(var), self.base))))

    def simplify(self):
        base = self.base.simplify()
        if isinstance(self.power, Expr):
            power = self.power.simplify()
        else:
            power = self.power
        if isinstance(power, (int, float)) and power == 0: return Const(1)
        if isinstance(power, Const) and power.value == 0: return Const(1)
        if isinstance(power, (int, float)) and power == 1: return base
        if isinstance(power, Const) and power.value == 1: return base
        if isinstance(base, Const) and isinstance(power, (int, float)): return Const(base.value ** power)
        if isinstance(base, Const) and isinstance(power, Const): return Const(base.value ** power.value)
        if isinstance(base, Const) and base.value == 0: return Const(0)
        return Pow(base, power)

    def subs(self, mapping):
        base = self.base.subs(mapping)
        power = self.power.subs(mapping) if isinstance(self.power, Expr) else self.power
        return Pow(base, power)

    def eval(self):
        base = self.base.eval()
        power = self.power.eval() if isinstance(self.power, Expr) else self.power
        return base ** power

    def __str__(self):
        return f"({self.base}^{self.power})"


class Sin(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Cos(self.expr), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.sin(expr.value))
        return Sin(expr)

    def subs(self, mapping): return Sin(self.expr.subs(mapping))
    def eval(self): return math.sin(self.expr.eval())

    def __str__(self):
        return f"sin({self.expr})"


class Cos(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Mul(Const(-1), Sin(self.expr)), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.cos(expr.value))
        return Cos(expr)

    def subs(self, mapping): return Cos(self.expr.subs(mapping))
    def eval(self): return math.cos(self.expr.eval())

    def __str__(self):
        return f"cos({self.expr})"


class Tan(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Add(1, Pow(Tan(self.expr), 2))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.tan(expr.value))
        return Tan(expr)

    def subs(self, mapping): return Tan(self.expr.subs(mapping))
    def eval(self): return math.tan(self.expr.eval())

    def __str__(self):
        return f"tan({self.expr})"


class Exp(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Exp(self.expr), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.exp(expr.value))
        return Exp(expr)

    def subs(self, mapping): return Exp(self.expr.subs(mapping))
    def eval(self): return math.exp(self.expr.eval())

    def __str__(self):
        return f"exp({self.expr})"


class Ln(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Pow(self.expr, -1), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Exp):
            return expr.expr
        return Ln(expr)

    def subs(self, mapping): return Ln(self.expr.subs(mapping))
    def eval(self): return math.log(self.expr.eval())

    def __str__(self):
        return f"ln({self.expr})"


class LogBase(Expr):
    def __init__(self, base, expr):
        self.base = base
        self.expr = ensure_expr(expr)

    def to_ln(self):
        base_val = self.base.val if hasattr(self.base, 'val') else self.base
        return Mul(Ln(self.expr), Const(1 / math.log(float(base_val))))

    def diff(self, var): return self.to_ln().diff(var)
    def subs(self, mapping): return LogBase(self.base, self.expr.subs(mapping))
    def eval(self): return math.log(self.expr.eval(), self.base)

    def __str__(self):
        return f"log_{self.base}({self.expr})"


class ExpBase(Expr):
    def __init__(self, base, expr):
        self.base = base
        self.expr = ensure_expr(expr)

    def to_exp(self): return Exp(Mul(Const(math.log(self.base)), self.expr))
    def diff(self, var): return self.to_exp().diff(var)
    def subs(self, mapping): return ExpBase(self.base, self.expr.subs(mapping))
    def eval(self): return self.base ** self.expr.eval()

    def __str__(self):
        return f"{self.base}^({self.expr})"


class Asin(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var):
        return Div(self.expr.diff(var), Pow(Add(Const(1), Mul(Const(-1), Pow(self.expr, 2))), Const(1/2)))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.asin(expr.value))
        return Asin(expr)

    def subs(self, mapping): return Asin(self.expr.subs(mapping))
    def eval(self): return math.asin(self.expr.eval())

    def __str__(self):
        return f"asin({self.expr})"


class Acos(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var):
        return Mul(Const(-1),
                   Div(self.expr.diff(var), Pow(Add(Const(1), Mul(Const(-1), Pow(self.expr, 2))), Const(1/2))))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.acos(expr.value))
        return Acos(expr)

    def subs(self, mapping): return Acos(self.expr.subs(mapping))
    def eval(self): return math.acos(self.expr.eval())

    def __str__(self):
        return f"acos({self.expr})"


class Atan(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Div(self.expr.diff(var), Add(Const(1), Pow(self.expr, 2)))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.atan(expr.value))
        return Atan(expr)

    def subs(self, mapping): return Atan(self.expr.subs(mapping))
    def eval(self): return math.atan(self.expr.eval())

    def __str__(self):
        return f"atan({self.expr})"


class Sinh(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Cosh(self.expr), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.sinh(expr.value))
        return Sinh(expr)

    def subs(self, mapping): return Sinh(self.expr.subs(mapping))
    def eval(self): return math.sinh(self.expr.eval())

    def __str__(self):
        return f"sinh({self.expr})"


class Cosh(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(Sinh(self.expr), self.expr.diff(var))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.cosh(expr.value))
        return Cosh(expr)

    def subs(self, mapping): return Cosh(self.expr.subs(mapping))
    def eval(self): return math.cosh(self.expr.eval())

    def __str__(self):
        return f"cosh({self.expr})"


class Tanh(Expr):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def diff(self, var): return Mul(self.expr.diff(var), Add(Const(1), Mul(Const(-1), Pow(Tanh(self.expr), 2))))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Const):
            return Const(math.tanh(expr.value))
        return Tanh(expr)

    def subs(self, mapping): return Tanh(self.expr.subs(mapping))
    def eval(self): return math.tanh(self.expr.eval())

    def __str__(self):
        return f"tanh({self.expr})"