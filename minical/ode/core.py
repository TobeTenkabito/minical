from abc import ABC, abstractmethod


_OP_REGISTRY = {}


def register_op(name):
    def wrapper(cls):
        _OP_REGISTRY[name] = cls
        cls.op_name = name
        return cls
    return wrapper


def make_op(name, *args):
    if name not in _OP_REGISTRY:
        raise KeyError(f"Operator '{name}' is not registered")
    return _OP_REGISTRY[name](*args)


class Expr(ABC):

    @abstractmethod
    def eval(self, env: dict):
        pass

    @abstractmethod
    def diff(self, var: str):
        pass

    def __add__(self, other):
        return make_op("add", self, _ensure_expr(other))

    def __radd__(self, other):
        return make_op("add", _ensure_expr(other), self)

    def __mul__(self, other):
        return make_op("mul", self, _ensure_expr(other))

    def __rmul__(self, other):
        return make_op("mul", _ensure_expr(other), self)

    def __neg__(self):
        return make_op("neg", self)


def _ensure_expr(x):
    if isinstance(x, Expr):
        return x
    return make_op("const", x)
