import re

from .model import ODE
from .ops import Var, Const
from .funcs import sin, cos, exp, log


def ode_from_latex(src):
    if isinstance(src, str):
        lines = [l.strip() for l in src.splitlines() if l.strip()]
    else:
        lines = src

    equations = [_parse_equation(line) for line in lines]

    return _build_ode_system(equations)


def _parse_equation(line):
    if "=" not in line:
        raise SyntaxError("ODE must contain '='")
    lhs, rhs = line.split("=", 1)
    return lhs.strip(), rhs.strip()


def _build_ode_system(equations):
    vars = []
    rhs = []

    aux_vars = {}

    for lhs, rhs_latex in equations:
        m2 = _parse_second_order(lhs)
        if m2:
            x = m2
            v = Var(f"d{x.name}")
            vars.append(x)
            rhs.append(v)
            expr = _parse_rhs(rhs_latex)
            vars.append(v)
            rhs.append(expr)

            continue
        x = _parse_first_order(lhs)
        expr = _parse_rhs(rhs_latex)

        vars.append(x)
        rhs.append(expr)

    return ODE(vars=vars, rhs=rhs)


_DXDT = re.compile(r"\\frac\{d([a-zA-Z]+)\}\{dt\}")
_D2XDT2 = re.compile(r"\\frac\{d\^2([a-zA-Z]+)\}\{dt\^2\}")
_PRIME1 = re.compile(r"([a-zA-Z]+)\'")
_PRIME2 = re.compile(r"([a-zA-Z]+)\'\'")


def _parse_first_order(lhs):
    lhs = lhs.replace(" ", "")

    m = _DXDT.fullmatch(lhs)
    if m:
        return Var(m.group(1))

    m = _PRIME1.fullmatch(lhs)
    if m:
        return Var(m.group(1))

    raise SyntaxError(f"Unsupported LHS: {lhs}")


def _parse_second_order(lhs):
    lhs = lhs.replace(" ", "")

    m = _D2XDT2.fullmatch(lhs)
    if m:
        return Var(m.group(1))

    m = _PRIME2.fullmatch(lhs)
    if m:
        return Var(m.group(1))

    return None


_TOKEN_RE = re.compile(
    r"""
    (?P<NUMBER>\d+(\.\d+)?) |
    (?P<FUNC>\\sin|\\cos|\\exp|\\log) |
    (?P<NAME>[a-zA-Z]+) |
    (?P<PLUS>\+) |
    (?P<MINUS>-) |
    (?P<MUL>\*) |
    (?P<FRAC>\\frac) |
    (?P<POW>\^) |
    (?P<LPAREN>\() |
    (?P<RPAREN>\)) |
    (?P<LBRACE>\{) |
    (?P<RBRACE>\})
    """,
    re.VERBOSE,
)

_FUNC_MAP = {
    "\\sin": sin,
    "\\cos": cos,
    "\\exp": exp,
    "\\log": log,
}


def _tokenize(src):
    return [(m.lastgroup, m.group()) for m in _TOKEN_RE.finditer(src)]


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def pop(self):
        t = self.peek()
        self.pos += 1
        return t

    def parse(self):
        return self.expr(0)

    def expr(self, rbp):
        t = self.pop()
        left = self.nud(t)
        while True:
            tok = self.peek()
            if not tok or self.lbp(tok) <= rbp:
                break
            t = self.pop()
            left = self.led(t, left)
        return left

    def nud(self, tok):
        k, v = tok
        if k == "NUMBER":
            return Const(float(v))
        if k == "NAME":
            return Var(v)
        if k == "MINUS":
            return -self.expr(100)
        if k == "FUNC":
            f = _FUNC_MAP[v]
            self.pop()  # (
            e = self.expr(0)
            self.pop()  # )
            return f(e)
        if k == "FRAC":
            self.pop()
            num = self.expr(0)
            self.pop()
            self.pop()
            den = self.expr(0)
            self.pop()
            return num / den
        if k == "LPAREN":
            e = self.expr(0)
            self.pop()
            return e
        raise SyntaxError(tok)

    def led(self, tok, left):
        k, _ = tok
        if k == "PLUS":
            return left + self.expr(10)
        if k == "MINUS":
            return left - self.expr(10)
        if k == "MUL":
            return left * self.expr(20)
        if k == "POW":
            return left ** self.expr(30)
        raise SyntaxError(tok)

    def lbp(self, tok):
        return {"PLUS": 10, "MINUS": 10, "MUL": 20, "POW": 30}.get(tok[0], 0)


def _parse_rhs(src):
    tokens = _tokenize(src.replace(" ", ""))
    return _Parser(tokens).parse()
