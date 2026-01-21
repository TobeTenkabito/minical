import re
from .core import Var, Const
from .ops import Add, Mul, Div, Pow, Sub
from .funcs import (
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh, exp, ln, logbase, sqrt,
    PI, E
)

FUNC_MAP = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'exp': exp, 'ln': ln, 'sqrt': sqrt
}

TOKEN_RE = re.compile(r"""
    (?P<FLOAT>\d+\.\d+) |
    (?P<INT>\d+) |
    (?P<CMD>\\[a-zA-Z]+) |
    (?P<OP>[\+\-\*/\^=]) |
    (?P<LBRACE>[\(\{]) |
    (?P<RBRACE>[\)\}]) |
    (?P<VAR>[a-zA-Z]) |
    (?P<UNDERSCORE>_) |
    (?P<COMMA>,) |
    (?P<SPACE>\s+)
""", re.VERBOSE)


def tokenize(s: str):
    for m in TOKEN_RE.finditer(s):
        kind = m.lastgroup
        if kind == "SPACE":
            continue
        yield (kind, m.group())
    yield ("EOF", "")


class LatexParser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.greek_vars = {
            '\\alpha', '\\beta', '\\gamma', '\\delta', '\\epsilon', '\\zeta',
            '\\eta', '\\theta', '\\iota', '\\kappa', '\\lambda', '\\mu',
            '\\nu', '\\xi', '\\pi', '\\rho', '\\sigma', '\\tau', '\\phi',
            '\\chi', '\\psi', '\\omega'
        }

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return ("EOF", "")

    def consume(self, expected_kind=None, expected_val=None):
        kind, val = self.peek()
        if expected_kind and kind != expected_kind:
            raise ValueError(f"Expected {expected_kind}, got {kind}")
        self.pos += 1
        return kind, val

    def parse(self):
        return self.parse_add()

    def parse_add(self):
        left = self.parse_mul()
        while True:
            _, val = self.peek()
            if val == '+':
                self.consume()
                left = Add(left, self.parse_mul())
            elif val == '-':
                self.consume()
                left = Sub(left, self.parse_mul())
            else:
                break
        return left

    def parse_mul(self):
        left = self.parse_pow()
        while True:
            kind, val = self.peek()
            if val in ('*', '\\cdot', '\\times'):
                self.consume()
                left = Mul(left, self.parse_pow())
            elif val in ('/', '\\div'):
                self.consume()
                left = Div(left, self.parse_pow())
            elif self._is_start_of_atom(kind, val):
                left = Mul(left, self.parse_pow())
            else:
                break
        return left

    def _is_start_of_atom(self, kind, val):
        if kind in ("INT", "FLOAT", "VAR", "LBRACE"): return True
        if kind == "CMD" and val not in ('\\cdot', '\\times', '\\div', '\\right'): return True
        return False

    def parse_pow(self):
        base = self.parse_atom()
        if self.peek()[1] == '^':
            self.consume()
            base = Pow(base, self.parse_atom())
        return base

    def parse_atom(self):
        kind, val = self.peek()
        if kind == "FLOAT": return Const(float(self.consume()[1]))
        if kind == "INT": return Const(int(self.consume()[1]))
        if kind == "VAR":
            var_name = self.consume()[1]
            if self.peek()[1] == '_':
                self.consume()
                sub = self.parse_group_content()
                var_name = f"{var_name}_{sub}"
            return Var(var_name)
        if kind == "LBRACE":
            self.consume()
            expr = self.parse_add()
            self.consume()
            return expr
        if kind == "CMD":
            return self.parse_command(val)
        raise ValueError(f"Unknown token: {val}")

    def parse_command(self, cmd):
        self.consume()
        if cmd == '\\left':
            self.consume()  # bracket
            expr = self.parse_add()
            self.consume()  # \right
            self.consume()  # bracket
            return expr
        if cmd == '\\frac':
            return Div(self.parse_group_content(), self.parse_group_content())
        if cmd == '\\sqrt':
            if self.peek()[1] == '[':
                self.consume()
                degree = self.parse_add()
                self.consume()  # ]
                return Pow(self.parse_group_content(), Div(Const(1), degree))
            return sqrt(self.parse_group_content())
        if cmd == '\\log':
            base = Const(10)
            if self.peek()[1] == '_':
                self.consume()
                base = self.parse_group_content()
            return logbase(base, self.parse_atom())
        if cmd == '\\ln':
            return ln(self.parse_atom())
        if cmd == '\\pi': return PI()
        if cmd in self.greek_vars: return Var(cmd[1:])

        func_name = cmd[1:]
        if func_name in FUNC_MAP:
            power = None
            if self.peek()[1] == '^':
                self.consume()
                power = self.parse_atom()
            node = FUNC_MAP[func_name](self.parse_atom())
            return Pow(node, power) if power else node

        raise ValueError(f"Unknown command: {cmd}")

    def parse_group_content(self):
        kind, val = self.peek()
        if val == '{':
            self.consume()
            res = self.parse_add()
            self.consume()
            return res
        return self.parse_atom()


def parse_latex(s: str):
    return LatexParser(tokenize(s)).parse()
