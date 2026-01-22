from __future__ import annotations
from typing import Any, Dict, List, Tuple, Union
from .core import Expr, Var, Const, Add, Mul, Transpose, Inverse, Func
from .ops import add, mul, transpose, inverse, func
import math


Matrix = List[List[float]]


def mat_shape(m: Matrix) -> Tuple[int, int]:
    return len(m), len(m[0]) if m else (0, 0)


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    n, m = mat_shape(a)
    return [[a[i][j] + b[i][j] for j in range(m)] for i in range(n)]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    n, k = mat_shape(a)
    k2, m = mat_shape(b)
    assert k == k2, "Matrix multiplication shape mismatch"
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for t in range(k):
                res[i][j] += a[i][t] * b[t][j]
    return res


def mat_transpose(a: Matrix) -> Matrix:
    n, m = mat_shape(a)
    return [[a[i][j] for i in range(n)] for j in range(m)]


def mat_eye(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_det(m: Matrix) -> float:
    n, k = mat_shape(m)
    assert n == k, "Determinant only for square matrices"
    a = [row[:] for row in m]
    det = 1.0
    for i in range(n):
        pivot = i
        while pivot < n and abs(a[pivot][i]) < 1e-12:
            pivot += 1
        if pivot == n:
            return 0.0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            det *= -1
        det *= a[i][i]
        piv = a[i][i]
        for j in range(i + 1, n):
            factor = a[j][i] / piv
            for k in range(i, n):
                a[j][k] -= factor * a[i][k]
    return det


def mat_inverse(m: Matrix) -> Union[Matrix, None]:
    n, k = mat_shape(m)
    assert n == k, "Inverse only for square matrices"
    a = [row[:] for row in m]
    inv = mat_eye(n)

    for i in range(n):
        pivot = i
        while pivot < n and abs(a[pivot][i]) < 1e-12:
            pivot += 1
        if pivot == n:
            return None
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            inv[i], inv[pivot] = inv[pivot], inv[i]

        piv = a[i][i]
        if abs(piv) < 1e-12:
            return None
        inv[i] = [x / piv for x in inv[i]]
        a[i] = [x / piv for x in a[i]]
        for j in range(n):
            if j != i:
                factor = a[j][i]
                inv[j] = [inv[j][k] - factor * inv[i][k] for k in range(n)]
                a[j] = [a[j][k] - factor * a[i][k] for k in range(n)]

    return inv


def mat_pow(a: Matrix, k: int) -> Matrix:
    assert k >= 0 and isinstance(k, int)
    n, m = mat_shape(a)
    assert n == m, "Matrix power requires square matrix"
    res = mat_eye(n)
    base = a
    while k:
        if k & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        k >>= 1
    return res


def mat_exp(a: Matrix, terms: int = 20) -> Matrix:
    n, m = mat_shape(a)
    assert n == m, "Matrix exp requires square matrix"
    result = mat_eye(n)
    term = mat_eye(n)

    for k in range(1, terms):
        term = mat_mul(term, a)
        term = [[x / k for x in row] for row in term]
        result = mat_add(result, term)

    return result


def mat_sin(a: Matrix, terms: int = 20) -> Matrix:
    n, m = mat_shape(a)
    assert n == m, "Matrix sin requires square matrix"
    result = [[0]*n for _ in range(n)]
    term = a

    sign = 1
    for k in range(1, terms, 2):
        if sign == 1:
            result = mat_add(result, term)
        else:
            result = mat_add(result, [[-x for x in row] for row in term])
        term = mat_mul(term, mat_mul(a, a))
        term = [[x / ((k+1)*(k+2)) for x in row] for row in term]
        sign *= -1

    return result


def mat_cos(a: Matrix, terms: int = 20) -> Matrix:
    n, m = mat_shape(a)
    assert n == m, "Matrix cos requires square matrix"
    result = mat_eye(n)
    term = mat_eye(n)

    sign = 1
    for k in range(0, terms):
        if sign == 1:
            result = mat_add(result, term)
        else:
            result = mat_add(result, [[-x for x in row] for row in term])
        term = mat_mul(term, mat_mul(a, a))
        term = [[x / ((2*k+1)*(2*k+2)) for x in row] for row in term]
        sign *= -1

    return result


def is_diagonal_matrix(M):
    n = len(M)
    for i in range(n):
        for j in range(n):
            if i != j and abs(M[i][j]) > 1e-12:
                return False
    return True


def mat_log_numeric(M):
    if not is_diagonal_matrix(M):
        raise ValueError("Only diagonal numeric matrices supported for log")

    n = len(M)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        if M[i][i] <= 0:
            raise ValueError("Matrix log requires positive diagonal entries")
        res[i][i] = math.log(M[i][i])
    return res


def is_matrix(x: Any) -> bool:
    return isinstance(x, list) and x and isinstance(x[0], list)


def is_scalar(x: Any) -> bool:
    return isinstance(x, (int, float))


def eval_expr(expr: Expr, env: Dict[str, Any]) -> Any:
    if isinstance(expr, Const):
        if expr.name.isdigit():
            return float(expr.name)
        return expr

    if isinstance(expr, Var):
        return env.get(expr.name, expr)

    if isinstance(expr, Add):
        a = eval_expr(expr.a, env)
        b = eval_expr(expr.b, env)

        if is_matrix(a) and is_matrix(b):
            return mat_add(a, b)
        if is_scalar(a) and is_scalar(b):
            return a + b
        return Add(a, b)

    if isinstance(expr, Mul):
        a = eval_expr(expr.a, env)
        b = eval_expr(expr.b, env)

        if is_matrix(a) and is_matrix(b):
            return mat_mul(a, b)
        if is_scalar(a) and is_scalar(b):
            return a * b
        if is_scalar(a) and is_matrix(b):
            return [[a * x for x in row] for row in b]
        if is_matrix(a) and is_scalar(b):
            return [[x * b for x in row] for row in a]

        return Mul(a, b)

    if isinstance(expr, Transpose):
        a = eval_expr(expr.x, env)
        if is_matrix(a):
            return mat_transpose(a)
        return Transpose(a)

    if isinstance(expr, Inverse):
        a = eval_expr(expr.x, env)

        if is_matrix(a):
            inv = mat_inverse(a)
            if inv is None:
                return Inverse(expr.x)
            return inv
        return Inverse(expr.x)

    if isinstance(expr, Func):
        evaluated_args = [eval_expr(a, env) for a in expr.args]
        if all(is_scalar(x) for x in evaluated_args):
            return eval_scalar_func(expr.name, evaluated_args)
        if expr.name == "pow" and len(evaluated_args) == 2:
            base, expn = evaluated_args
            if is_matrix(base) and isinstance(expn, (int, float)) and float(expn).is_integer():
                return mat_pow(base, int(expn))

        if expr.name == "exp" and len(evaluated_args) == 1:
            if is_matrix(evaluated_args[0]):
                return mat_exp(evaluated_args[0])

        if expr.name == "sin" and len(evaluated_args) == 1:
            if is_matrix(evaluated_args[0]):
                return mat_sin(evaluated_args[0])

        if expr.name == "cos" and len(evaluated_args) == 1:
            if is_matrix(evaluated_args[0]):
                return mat_cos(evaluated_args[0])
        if expr.name == "ln":
            arg = evaluated_args[0]
            if is_matrix(arg):
                try:
                    return mat_log_numeric(arg)
                except Exception:
                    return expr
        return Func(expr.name, tuple(evaluated_args))
    return expr


def eval_scalar_func(name: str, args: List[Any]) -> Any:
    if name == "exp":
        return math.exp(args[0])
    if name in ("ln", "log"):
        return math.log(args[0])
    if name == "sin":
        return math.sin(args[0])
    if name == "cos":
        return math.cos(args[0])
    if name == "tan":
        return math.tan(args[0])
    if name == "sinh":
        return math.sinh(args[0])
    if name == "cosh":
        return math.cosh(args[0])
    if name == "tanh":
        return math.tanh(args[0])
    if name == "asin":
        return math.asin(args[0])
    if name == "acos":
        return math.acos(args[0])
    if name == "atan":
        return math.atan(args[0])
    if name == "pow":
        return math.pow(args[0], args[1])
    raise ValueError(f"Unknown scalar function: {name}")
