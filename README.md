# MiniCal

**MiniCal** is a minimal symbolic calculus engine written in pure Python.  
It focuses on **symbolic differentiation**, **LaTeX expression parsing**, and **numerical validation**, with an emphasis on clarity, extensibility, and mathematical correctness.

Unlike full-featured CAS systems, MiniCal is designed to be **small, inspectable, and hackable**, making it suitable for experimentation, learning, and research-oriented extensions.

---
## Reason
If you've read this far, you might be wondering why I wrote this code. 
The answer is actually quite simple: bored people always want to find something interesting to do. 
Although the tools for finding derivatives are now very sophisticated, 
isn't there a certain fun in building something from scratch, bit by bit?

---

## Features

- Symbolic differentiation  
  - First-order, higher-order, and mixed partial derivatives
- Expression tree (AST)–based representation
- Built-in LaTeX parser (no third-party CAS dependency)
- Expression simplification
- Numerical derivative validation via finite differences
- Supports nested and composite expressions
- Simple matrix algebra operations and numerical calculations

---

## Example

```python
from minical.symdiff import parse_latex, diff, full_simplify

expr = parse_latex(r"""
\ln\left(\frac{\sin^2(x^2) + \sqrt{y}}
{ \exp(x) + \log_{2}(x+y)}\right)
+ \frac{\tan(\frac{x}{y})}{\sqrt[3]{\sin(x) + \cos(y)}}
""")

dx = full_simplify(diff(expr, "x"))
dy = full_simplify(diff(expr, "y"))

print("∂/∂x:", dx)
print("∂/∂y:", dy)
```

### Higher-Order and Mixed Derivatives
MiniCal supports chained differentiation:
```python
# Third-order derivative with respect to x
d3x = diff(expr, "x").diff("x").diff("x")

# Mixed partial derivative ∂³ / (∂x² ∂y)
d2x1y = diff(expr, "x").diff("x").diff("y")
```
All derivatives are represented symbolically and can be further simplified or evaluated.

### Numerical Validation
Symbolic derivatives can be validated numerically using finite differences:
```python
from minical.symdiff import validate

point = {"x": 2.0, "y": 1.0}

validate(expr, dx, "x", point)
validate(expr, d3x, ["x", "x", "x"], point, tol=1e-3)
```
#### This is especially useful for:
    Debugging differentiation rules
    Verifying higher-order derivatives
    Detecting simplification errors

Note: numerical validation of high-order derivatives is sensitive to step size and floating-point error.
Tolerance can be adjusted by the user.

### matrix calculus
```python
from minical.matrix import Var, exp, sin, cos, pow, Inverse, eval_expr,ln

A = Var("A", (2,2))
B = Var("B", (2,2))
env = { "A": [[1, 2],[3, 4]],"B": [[1, 2],[2, 4]] }
expr1 = pow(A, 2)
print("pow(A,2) =", eval_expr(expr1, env))
expr2 = exp(A)
print("exp(A) =", eval_expr(expr2, env))
expr3 = sin(A)
expr4 = cos(A)
print("sin(A) =", eval_expr(expr3, env))
print("cos(A) =", eval_expr(expr4, env))
expr5 = Inverse(B)
print("Inverse(B) =", eval_expr(expr5, env))
expr6 = exp(A) @ Inverse(A)
print("exp(A) * inv(A) =", eval_expr(expr6, env))
```
### the output would be
```python
pow(A,2) = [[7, 10], [15, 22]]
exp(A) = [[51.96890355105711, 74.73648783689403], [112.10473175534102, 164.0736353063982]]
sin(A) = [[-0.46559101168184286, -0.14843834244287693], [-0.2226575136643153, -0.688248525346158]]
cos(A) = [[1.8554231650779978, -0.11087638101074773], [-0.166314571516122, 1.6891085935618741]]
Inverse(B) = (B^-1)
exp(A) * inv(A) = [[8.166924653226829, 14.600659632610096], [21.900989448915254, 30.067914102141927]]
```

## Design Philosophy
#### Minimalism over completeness
Only core calculus primitives are implemented.
#### No heavy dependencies
MiniCal does not rely on SymPy or other CAS libraries.
#### Explicit structure
Expressions are represented as AST nodes, not strings.
#### Extensibility first
New operators, functions, or calculus modules can be added incrementally.

## Project Structure
```graphql
minical/
├── symdiff/
│   ├── core.py        # Base expression classes
│   ├── ops.py         # Binary and unary operators
│   ├── funcs.py       # Elementary functions
│   ├── diff.py        # Differentiation rules
│   ├── simplify.py   # Simplification logic
│   ├── latex.py      # LaTeX parser
│   ├── validate.py   # Numerical derivative validation
│   └── __init__.py
├── matrix/
│   ├── calculus.py
│   ├── core.py
│   ├── funcs.py
│   ├── ops.py
│   ├── simplify.py
│   └── __init__.py
├── ode/
│   ├── calculus.py
│   ├── core.py
│   ├── funcs.py
│   ├── latex.py
│   ├── model.py
│   ├── ops.py
│   ├── simplify.py
│   └── __init__.py
├── statistiques/
│   ├── core.py
│   ├── correlation.py
│   ├── covariance.py
│   ├── credible_interval.py
│   ├── discrete.py
│   ├── distributions.py
│   ├── expectation.py
│   ├── funcs.py
│   ├── ops.py
│   ├── posterior_predictive.py
│   ├── process.py
│   ├── sampling.py
│   ├── sde.py
│   ├── timeseries.py
│   ├── variance.py
│   ├── __init__.py
│   ├── analysis/
│   │   ├── coupling.py
│   │   ├── functionals.py
│   │   └── __init__.py
│   ├── bayes/
│   │   ├── core.py
│   │   ├── linear.py
│   │   ├── normal.py
│   │   └── __init__.py
│   └── control/
│   │   ├── hjb/
│   │   │   ├── policy.py
│   │   │   ├── problem.py
│   │   │   └── __init__.py
│   │   ├── pontryagin/
│   │   │   ├── adjoint.py
│   │   │   ├── policy.py
│   │   │   ├── problem.py
│   │   │   ├── sovler.py
│   │   │   └── __init__.py
│   │   └── __init__.py
```
