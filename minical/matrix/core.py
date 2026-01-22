from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Any

Shape = Tuple[int, int]

class Expr:
    shape: Shape

    def simplify(self) -> Expr:
        from .simplify import simplify
        return simplify(self)

    def __add__(self, other: Expr) -> Expr:
        from .ops import add
        return add(self, other)

    def __matmul__(self, other: Expr) -> Expr:
        from .ops import mul
        return mul(self, other)

    @property
    def T(self) -> Expr:
        from .ops import transpose
        return transpose(self)

    @property
    def inv(self) -> Expr:
        from .ops import inverse
        return inverse(self)

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Expr) and str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))

@dataclass(frozen=True)
class Var(Expr):
    name: str
    shape: Shape

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Const(Expr):
    name: str
    shape: Shape

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Add(Expr):
    a: Expr
    b: Expr

    def __post_init__(self):
        if self.a.shape != self.b.shape:
            raise ValueError("Shape mismatch for Add")
        object.__setattr__(self, "shape", self.a.shape)

    def __str__(self):
        return f"({self.a} + {self.b})"


@dataclass(frozen=True)
class Mul(Expr):
    a: Expr
    b: Expr

    def __post_init__(self):
        if self.a.shape[1] != self.b.shape[0]:
            raise ValueError("Shape mismatch for Mul")
        object.__setattr__(self, "shape", (self.a.shape[0], self.b.shape[1]))

    def __str__(self):
        return f"({self.a} * {self.b})"


@dataclass(frozen=True)
class Transpose(Expr):
    x: Expr

    def __post_init__(self):
        object.__setattr__(self, "shape", (self.x.shape[1], self.x.shape[0]))

    def __str__(self):
        return f"({self.x}^T)"


@dataclass(frozen=True)
class Inverse(Expr):
    x: Expr

    def __post_init__(self):
        if self.x.shape[0] != self.x.shape[1]:
            raise ValueError("Inverse requires square matrix")
        object.__setattr__(self, "shape", self.x.shape)

    def __str__(self):
        return f"({self.x}^-1)"


@dataclass(frozen=True)
class Scalar(Expr):
    name: str


@dataclass(frozen=True)
class ScalarFunc(Expr):
    func: str
    x: Expr


@dataclass(frozen=True)
class ScalarMul(Expr):
    scalar: Expr
    mat: Expr


@dataclass(frozen=True)
class ScalarAdd(Expr):
    scalar: Expr
    mat: Expr
    def __post_init__(self):
        object.__setattr__(self, "shape", self.mat.shape)

    def __str__(self):
        return f"({self.mat} + {self.scalar})"


@dataclass(frozen=True)
class Func(Expr):
    name: str
    args: Tuple[Expr, ...]

    def __post_init__(self):
        if not self.args:
            object.__setattr__(self, "shape", (1, 1))
            return
        first = self.args[0]
        if hasattr(first, "shape"):
            object.__setattr__(self, "shape", first.shape)
            return
        if isinstance(first, list) and first and isinstance(first[0], list):
            object.__setattr__(self, "shape", (len(first), len(first[0])))
            return
        object.__setattr__(self, "shape", (1, 1))

    def __str__(self):
        args_str = ", ".join(str(a) for a in self.args)
        return f"{self.name}({args_str})"
