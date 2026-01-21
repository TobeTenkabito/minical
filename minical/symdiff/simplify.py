def full_simplify(expr):
    prev = None
    cur = expr
    while str(prev) != str(cur):
        prev = cur
        cur = cur.simplify()
    return cur
