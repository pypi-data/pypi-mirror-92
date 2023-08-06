class Test(object):
    """
        >>> import pytetgen
        >>> import numpy as np
        >>> N = 4
        >>> points = np.random.random(3*N).reshape(N,3)
        >>> tri = pytetgen.Delaunay(points)
        >>> np.sort(tri.simplices)
        array([[0, 1, 2, 3]], dtype=int32)

    """
    pass
