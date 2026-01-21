from .core import Var, vars, Const, Expr, ensure_expr
from .funcs import sin, cos, exp, ln
from .calculus import diff
from .simplify import full_simplify
from .latex import parse_latex
from .validate import validate

import logging

logging.basicConfig(
    filename="symdlff.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

