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
```
