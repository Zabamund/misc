import numpy as np

def euclidian_dist(ax, ay, bx, by):
    """Return the Euclidian distance between two points a and b
    where a has coords ax, ay and b has coords bx, by
    Examples
    --------
    >>> euclidian_dist(0, 0, 1, 1)
    1.4142135623730951
    >>> euclidian_dist(0, 0, -1, -1)
    1.4142135623730951
    """
    return np.sqrt((bx - ax)**2 + (by - ay)**2)


def minkowski_dist(xs, ys, p=1):
    xs, ys = np.array(xs), np.array(ys)
    if np.isinf(p):
        return np.max(np.abs(xs - ys))
    elif np.isneginf(p):
        return np.min(np.abs(xs - ys))
    else:
        return np.sum(np.abs(xs - ys)**p)**(1/p)