from .simplify import simplify
from .core import Expr
from .ops import Var


class ODE:
    def __init__(self, vars, rhs, params=None, events=None):
        assert len(vars) == len(rhs)

        self.vars = vars
        self.rhs_expr = [simplify(e) for e in rhs]
        self._jac_expr = None
        self.params = params or []
        self.events = events or []


    def f(self):
        vars = self.vars
        rhs = self.rhs_expr

        def f_num(t, y):
            env = {"t": t}
            env.update({v.name: y[i] for i, v in enumerate(vars)})
            return [expr.eval(env) for expr in rhs]

        return f_num

    def jac(self):
        if self._jac_expr is None:
            self._jac_expr = [
                [simplify(expr.diff(v.name)) for v in self.vars]
                for expr in self.rhs_expr
            ]

        vars = self.vars
        jac = self._jac_expr

        def jac_num(t, y):
            env = {"t": t}
            env.update({v.name: y[i] for i, v in enumerate(vars)})
            return [
                [expr.eval(env) for expr in row]
                for row in jac
            ]

        return jac_num