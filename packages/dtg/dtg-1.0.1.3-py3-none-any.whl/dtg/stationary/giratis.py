import numpy as np


def stat(data, q=None):
    ns = data.size
    mn = np.mean(data)

    if q is None:
        q = int(np.sqrt(ns))

    dels = data - mn
    s = np.array([np.sum(dels[: i + 1]) for i in np.arange(dels.size)])
    gamma = []
    for _ in np.arange(q):
        for j in np.arange(q):
            gamma.append(np.sum(np.multiply(dels[: ns - j], dels[j:])) / ns)

    v = (np.sum(s ** 2) - (np.sum(s) ** 2 / ns)) / (ns ** 2)
    s = np.sum(gamma) / q
    if s == 0:
        return 0
    return np.abs(v / s)
