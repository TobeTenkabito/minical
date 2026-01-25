# statistiques

`statistiques` is the probability, statistics, and stochastic systems submodule of **minical**.

It provides a lightweight, dependency-free framework for:

- Symbolic random variables
- Probability distributions
- Monte Carlo sampling
- Statistical operators
- Bayesian inference and prediction
- Discrete-time stochastic processes
- Stochastic differential equations (SDE)
- Pathwise statistical analysis
- Uncertainty-aware control methods

Design goals:

- Minimal
- Composable
- Explicit
- No third-party dependencies

---

## Public API

All examples below assume:

```python
from minical.statistiques import *
```

The public API is defined by `statistiques/__init__.py`.

---

## 1. Core Random Variable System

### Random Variables and Constants

```python
X = RV()
c = Const(2.0)
```

Random variables support symbolic composition and delayed evaluation.

---

## 2. Probability Distributions

```python
X = Normal(0.0, 1.0)
Y = Uniform(-1.0, 1.0)
```

Distributions are random variables and can be combined algebraically.

---

## 3. Algebra on Random Variables

```python
Z = 2 * X + X**2 - 1
```

All operations construct symbolic expression trees.

---

## 4. Elementary Functions

```python
Y = exp(X) + abs(X)
Z = sin(X) * cos(X)
```

Supported functions:

- `sin`
- `cos`
- `exp`
- `log`
- `abs`

---

## 5. Monte Carlo Sampling

```python
samples = sample(Z, 100_000)
mean_est = sum(samples) / len(samples)
```

All numerical evaluation is performed via Monte Carlo sampling.

---

## 6. Statistical Operators

### Expectation

```python
E(X)
E(X + 1)
```

### Variance

```python
var(X)
```

### Covariance and Correlation

```python
cov(X, Y)
corr(X, Y)
```

---

## 7. Bayesian Inference

### Posterior Predictive Distribution

```python
pp = posterior_predictive(prior=X, likelihood=Y)
```

### Credible Interval

```python
credible_interval(pp, level=0.95)
```

### Predictive Summary

```python
predictive_summary(pp)
```

---

## 8. Discrete-Time Stochastic Processes

### Random Walk

```python
rw = RandomWalk(sigma=1.0, x0=0.0)
paths = rw.simulate(n_steps=100, n_paths=1000)
```

### AR(1) Process

```python
ar = AR1(phi=0.8, sigma=1.0, x0=0.0)
paths = ar.simulate(n_steps=200, n_paths=500)
```

---

## 9. Stochastic Differential Equations (SDE)

```python
def drift(x, t):
    return 0.1 * x

def diffusion(x, t):
    return 0.2 * x

sde = SDE(drift, diffusion, x0=1.0, dt=0.01)
paths = sde.simulate(T=1.0, n_samples=5000)
```

Supported schemes include Euler–Maruyama and Milstein.

---

## 10. Pathwise Analysis

Path-level statistics are available via the `analysis` namespace.

```python
from minical.statistiques import analysis
```

Examples:

```python
analysis.path_max(paths)
analysis.path_min(paths)
analysis.terminal_mean(paths)
analysis.hitting_time(paths, threshold=2.0)
```

---

## 11. Bayesian Methods Namespace

```python
from minical.statistiques import bayes
```

Contains Bayesian updating and inference utilities.

---

## 12. Control Namespace

```python
from minical.statistiques import control
```

Provides uncertainty-aware control methods for stochastic systems
(e.g. SDE control, HJB, PMP).

---

## Design Principles

- All uncertain quantities are modeled as random variables
- Expression construction is separated from numerical evaluation
- Sampling is the only numerical backend
- Distributions, processes, and control methods are composable

---

## Current Scope

Supported:

- Scalar random variables
- Monte Carlo inference
- Discrete and continuous stochastic processes
- Pathwise statistics
- Bayesian prediction
- Uncertainty-aware control frameworks

Not supported:

- Automatic differentiation
- Closed-form symbolic solutions
- High-dimensional vectorized backends

---

## Intended Use Cases

- Probability and stochastic process education
- Monte Carlo prototyping
- Bayesian modeling
- Stochastic system simulation
- Integration with ODE and control modules

---

## Status

This module is designed as a long-term, extensible core of the `minical` ecosystem.
Public APIs defined here are intended to remain stable.
