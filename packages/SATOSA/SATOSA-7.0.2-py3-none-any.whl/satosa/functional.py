def identity(f):
    return f


def compose(f, g):
    c = g(f)
    return c
