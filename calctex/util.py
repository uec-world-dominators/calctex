import numpy as np


def standard_uncertainty(x):
    N = len(x)
    ave = np.average(x)
    return (1/(N*(N-1))*np.sum((x-ave)**2))**0.5


def cumulative_tolerance(x):
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    return (np.sum(x**2, axis=0))**0.5


def with_uncertainty(x, uncertainty):
    if not isinstance(x, np.ndarray) or not isinstance(uncertainty, np.ndarray) or x.shape != uncertainty.shape:
        raise Exception('dimention error')
