from typing import Dict, Callable, Tuple
from .core import Func, Expr
from .ops import func


def exp(x: Expr) -> Expr:
    return func("exp", x)

def ln(x: Expr) -> Expr:
    return func("ln", x)

def log(x: Expr, base: Expr = None) -> Expr:
    if base is None:
        return func("log", x)
    return func("log", x, base)

def sin(x: Expr) -> Expr:
    return func("sin", x)

def cos(x: Expr) -> Expr:
    return func("cos", x)

def tan(x: Expr) -> Expr:
    return func("tan", x)

def sinh(x: Expr) -> Expr:
    return func("sinh", x)

def cosh(x: Expr) -> Expr:
    return func("cosh", x)

def tanh(x: Expr) -> Expr:
    return func("tanh", x)

def asin(x: Expr) -> Expr:
    return func("asin", x)

def acos(x: Expr) -> Expr:
    return func("acos", x)

def atan(x: Expr) -> Expr:
    return func("atan", x)

def pow(x: Expr, y: Expr) -> Expr:
    return func("pow", x, y)


FUNCTION_REGISTRY: Dict[str, Dict] = {
    "exp": {"inverse": "ln", "arity": 1},
    "ln": {"inverse": "exp", "arity": 1},
    "log": {"inverse": None, "arity": (1, 2)},
    "sin": {"inverse": "asin", "arity": 1},
    "cos": {"inverse": "acos", "arity": 1},
    "tan": {"inverse": "atan", "arity": 1},
    "sinh": {"inverse": None, "arity": 1},
    "cosh": {"inverse": None, "arity": 1},
    "tanh": {"inverse": None, "arity": 1},
    "asin": {"inverse": "sin", "arity": 1},
    "acos": {"inverse": "cos", "arity": 1},
    "atan": {"inverse": "tan", "arity": 1},
    "pow": {"inverse": None, "arity": 2},
}
