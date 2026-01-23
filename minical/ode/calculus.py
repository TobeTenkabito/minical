import math


class ODEResult:
    def __init__(self, ts, ys, status="success"):
        self.t = ts
        self.y = ys
        self.status = status


def solve(
    ode,
    t_span,
    y0,
    method="rk45",
    rtol=1e-6,
    atol=1e-9,
    h0=1e-3,
    h_min=1e-10,
    h_max=0.1,
    max_steps=100000
):
    m = method.lower()
    if m == "rk45":
        return _solve_rk45(
            ode, t_span, y0, rtol, atol, h0, h_min, h_max, max_steps
        )
    elif m == "implicit_euler":
        return _solve_implicit_euler(
            ode, t_span, y0, h0, max_steps
        )
    else:
        raise ValueError(f"Unknown method: {method}")


def _solve_rk45(
    ode, t_span, y0, rtol, atol, h0, h_min, h_max, max_steps
):
    f = ode.f()
    t0, tf = t_span
    t = t0
    y = list(y0)
    h = h0
    ts = [t]
    ys = [y.copy()]
    for _ in range(max_steps):
        if t >= tf:
            break
        if t + h > tf:
            h = tf - t
        y_new, err = _rk45_step(f, t, y, h)
        err_norm = _error_norm(y, y_new, err, rtol, atol)
        if err_norm <= 1.0:
            t += h
            y = y_new
            ts.append(t)
            ys.append(y.copy())
            if err_norm == 0.0:
                h *= 2.0
            else:
                h *= min(2.0, max(0.2, 0.9 * err_norm ** (-0.2)))
        else:
            h *= max(0.2, 0.9 * err_norm ** (-0.25))

        if h < h_min:
            return ODEResult(ts, ys, status="failed: step too small")

        h = min(h, h_max)

    return ODEResult(ts, ys)


def _rk45_step(f, t, y, h):
    k1 = f(t, y)

    k2 = f(t + h * 1/5, _lin(y, k1, h * 1/5))

    k3 = f(t + h * 3/10, _lin2(y, k1, 3/40, k2, 9/40, h))

    k4 = f(
        t + h * 4/5,
        _lin3(y, k1, 44/45, k2, -56/15, k3, 32/9, h),
    )

    k5 = f(
        t + h * 8/9,
        _lin4(
            y,
            k1, 19372/6561,
            k2, -25360/2187,
            k3, 64448/6561,
            k4, -212/729,
            h,
        ),
    )

    k6 = f(
        t + h,
        _lin5(
            y,
            k1, 9017/3168,
            k2, -355/33,
            k3, 46732/5247,
            k4, 49/176,
            k5, -5103/18656,
            h,
        ),
    )

    y4 = _lin5(
        y,
        k1, 35/384,
        k3, 500/1113,
        k4, 125/192,
        k5, -2187/6784,
        k6, 11/84,
        h,
    )

    k7 = f(t + h, y4)

    y5 = _lin6(
        y,
        k1, 5179/57600,
        k3, 7571/16695,
        k4, 393/640,
        k5, -92097/339200,
        k6, 187/2100,
        k7, 1/40,
        h,
    )

    err = [y5[i] - y4[i] for i in range(len(y))]
    return y4, err

def _solve_implicit_euler(
    ode,
    t_span,
    y0,
    h,
    max_steps,
    newton_tol=1e-8,
    newton_maxiter=20,
):
    f = ode.f()
    jac = ode.jac()
    if jac is None:
        raise ValueError("Implicit Euler requires Jacobian")

    t0, tf = t_span
    t = t0
    y = list(y0)

    ts = [t]
    ys = [y.copy()]

    for _ in range(max_steps):
        if t >= tf:
            break
        if t + h > tf:
            h = tf - t

        t_next = t + h
        y_guess = y.copy()
        for _ in range(newton_maxiter):
            fy = f(t_next, y_guess)
            G = [
                y_guess[i] - y[i] - h * fy[i]
                for i in range(len(y))
            ]

            norm = sum(abs(g) for g in G)
            if norm < newton_tol:
                break
            J = jac(t_next, y_guess)
            A = _implicit_matrix(J, h)
            delta = _solve_linear(A, G)
            alpha = 1.0
            for i in range(len(y)):
                y_guess[i] -= alpha * delta[i]
        else:
            return ODEResult(ts, ys, status="failed: Newton did not converge")

        # accept step
        t = t_next
        y = y_guess
        ts.append(t)
        ys.append(y.copy())

    return ODEResult(ts, ys)


def _implicit_matrix(J, h):
    n = len(J)
    A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = (-h * J[i][j])
        A[i][i] += 1.0
    return A


def _solve_linear(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Gaussian elimination
    for i in range(n):
        pivot = M[i][i]
        if abs(pivot) < 1e-14:
            raise ValueError("Singular matrix in Newton solve")

        for j in range(i, n + 1):
            M[i][j] /= pivot

        for k in range(n):
            if k == i:
                continue
            factor = M[k][i]
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]

    return [M[i][-1] for i in range(n)]


def _error_norm(y, y_new, err, rtol, atol):
    s = 0.0
    for i in range(len(y)):
        tol = atol + rtol * max(abs(y[i]), abs(y_new[i]))
        s += (err[i] / tol) ** 2
    return math.sqrt(s / len(y))


def _lin(y, k1, a1):
    return [y[i] + a1 * k1[i] for i in range(len(y))]


def _lin2(y, k1, a1, k2, a2, h):
    return [y[i] + h * (a1 * k1[i] + a2 * k2[i]) for i in range(len(y))]


def _lin3(y, k1, a1, k2, a2, k3, a3, h):
    return [
        y[i] + h * (a1 * k1[i] + a2 * k2[i] + a3 * k3[i])
        for i in range(len(y))
    ]


def _lin4(y, k1, a1, k2, a2, k3, a3, k4, a4, h):
    return [
        y[i] + h * (a1 * k1[i] + a2 * k2[i] + a3 * k3[i] + a4 * k4[i])
        for i in range(len(y))
    ]


def _lin5(y, k1, a1, k2, a2, k3, a3, k4, a4, k5, a5, h):
    return [
        y[i]
        + h * (a1 * k1[i] + a2 * k2[i] + a3 * k3[i] + a4 * k4[i] + a5 * k5[i])
        for i in range(len(y))
    ]


def _lin6(y, k1, a1, k2, a2, k3, a3, k4, a4, k5, a5, k6, a6, h):
    return [
        y[i]
        + h * (
            a1 * k1[i]
            + a2 * k2[i]
            + a3 * k3[i]
            + a4 * k4[i]
            + a5 * k5[i]
            + a6 * k6[i]
        )
        for i in range(len(y))
    ]
