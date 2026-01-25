from ..sampling import sample


def coupled_simulate(proc1, proc2, n_steps, n_samples=1000):
    paths1, paths2 = [], []

    for _ in range(n_samples):
        x1, x2 = proc1.x0, proc2.x0
        path1, path2 = [x1], [x2]

        for t in range(n_steps):
            expr1 = proc1.step(x1, t)
            expr2 = proc2.step(x2, t)

            # shared noise
            z = sample(expr1 - expr2, 1)[0]

            x1 = sample(expr1, 1)[0]
            x2 = x1 - z

            path1.append(x1)
            path2.append(x2)

        paths1.append(path1)
        paths2.append(path2)

    return paths1, paths2
