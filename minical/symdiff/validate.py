def numerical_diff(func_expr, var_name, point, h=1e-5, order=1):
    if order == 0:
        return func_expr.subs(point).eval()
    p_plus = point.copy()
    p_plus[var_name] += h

    p_minus = point.copy()
    p_minus[var_name] -= h

    if order == 1:
        v_plus = func_expr.subs(p_plus).eval()
        v_minus = func_expr.subs(p_minus).eval()
        return (v_plus - v_minus) / (2 * h)
    else:
        d_plus = _get_numerical_derivative_recursive(func_expr, [var_name] * (order - 1), p_plus, h)
        d_minus = _get_numerical_derivative_recursive(func_expr, [var_name] * (order - 1), p_minus, h)
        return (d_plus - d_minus) / (2 * h)


def _get_numerical_derivative_recursive(expr, vars_list, point, h):
    if not vars_list:
        return expr.subs(point).eval()

    current_var = vars_list[0]
    remaining_vars = vars_list[1:]

    p_plus = point.copy()
    p_plus[current_var] += h

    p_minus = point.copy()
    p_minus[current_var] -= h

    v_plus = _get_numerical_derivative_recursive(expr, remaining_vars, p_plus, h)
    v_minus = _get_numerical_derivative_recursive(expr, remaining_vars, p_minus, h)

    return (v_plus - v_minus) / (2 * h)


def check_derivative(original_expr, symbolic_derivative, vars_path, point, tol=1e-4):
    if isinstance(vars_path, str):
        vars_path = [vars_path]
    try:
        sym_val = symbolic_derivative.subs(point).eval()
    except Exception as e:
        return False, f"Symbolic Eval Error: {e}", 0
    try:
        num_val = _get_numerical_derivative_recursive(original_expr, vars_path, point, h=1e-5)
    except Exception as e:
        return False, sym_val, f"Numerical Eval Error: {e}"
    abs_error = abs(sym_val - num_val)
    if abs(num_val) > 1e-7:
        is_correct = (abs_error / abs(num_val)) < tol
    else:
        is_correct = abs_error < tol

    return is_correct, sym_val, num_val


def check_report(original_expr, symbolic_derivative, vars_path, point, label="Derivative"):
    passed, s_val, n_val = check_derivative(original_expr, symbolic_derivative, vars_path, point)
    status = "PASSED" if passed else "FAILED"
    print(f"--- {label} Check ---")
    print(f"Variables: {vars_path}")
    print(f"At point:  {point}")
    print(f"Symbolic:  {s_val}")
    print(f"Numerical: {n_val}")
    print(f"Status:    {status}")
    if not passed:
        diff_val = abs(s_val - n_val)
        print(f"Abs Diff:  {diff_val}")
    print("-" * (len(label) + 16))
    return passed


def validate(original_expr, symbolic_derivative, vars_path, point,
             tol=1e-4, verbose=True):
    passed, sym, num = check_derivative(
        original_expr,
        symbolic_derivative,
        vars_path,
        point,
        tol=tol
    )

    if verbose:
        check_report(
            original_expr,
            symbolic_derivative,
            vars_path,
            point,
            label="Derivative"
        )

    return passed
