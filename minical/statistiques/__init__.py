# ===== Core random variable system =====
from .core import RV, Const

# ===== Distributions =====
from .distributions import (
    Normal,
    Uniform,
)

# ===== Elementary functions =====
from .funcs import (
    sin,
    cos,
    exp,
    log,
    abs,
)

# ===== Statistical operators =====
from .expectation import E
from .variance import var
from .covariance import cov
from .correlation import corr
from .posterior_predictive import posterior_predictive
from .credible_interval import credible_interval, predictive_summary
from .sampling import sample
from .discrete import (
    AR1,
    RandomWalk,
)
from .sde import SDE
from . import analysis
from . import bayes
from . import control
__all__ = [
    # Core
    "RV", "Const",

    # Distributions
    "Normal", "Uniform",

    # Functions
    "sin", "cos", "exp", "log", "abs",

    # Statistics
    "E", "var", "cov", "corr",

    # Bayesian
    "posterior_predictive",
    "credible_interval",
    "predictive_summary",

    # Sampling
    "sample",

    # Processes
    "AR1", "RandomWalk", "SDE",

    # Method
    "analysis", "bayes", "control"
]
