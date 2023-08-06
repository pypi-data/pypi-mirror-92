import scipy.interpolate as si
import numpy as np


def b_spline(cv, n=100, degree=3):
    """
    source: https://stackoverflow.com/questions/28279060/splines-with-python-using-control-knots-and-endpoints

    Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree

    """
    cv = np.asarray(cv)
    count = cv.shape[0]

    # Prevent degree from exceeding count-1, otherwise splev will crash
    degree = np.clip(degree, 1, count-1)

    # Calculate knot vector
    kv = np.array([0]*degree + [i for i in range(count-degree+1)] + [count-degree]*degree, dtype='int')

    # Calculate query range
    u = np.linspace(0, (count-degree), n)

    # Calculate result
    return np.array(si.splev(u, (kv, cv.T, degree))).T.tolist()
