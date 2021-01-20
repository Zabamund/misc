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


