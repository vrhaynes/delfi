import numpy as np
from scipy.special import expit, logit, ndtr, ndtri
from scipy.stats import norm


def log_expit_deriv(y):
    x = expit(y)
    return np.log(x) + np.log(1 - x)


def log_logit_deriv(x):
    return -(np.log(x) + np.log(1 - x))


def named_bijection(name, **kwargs):
    name = name.lower()

    if name == 'logit':

        f = logit
        finv = expit
        f_jac_logD = lambda x: log_logit_deriv(x).sum(axis=-1)
        finv_jac_logD = lambda y: log_expit_deriv(y).sum(axis=-1)

    elif name == 'affine':

        s = kwargs['scale'].copy()
        o = kwargs['offset'].copy()
        f = lambda x: x * s + o
        finv = lambda y: (y - o) / s
        f_jac_logD = lambda x: np.log(s).sum(axis=-1)
        finv_jac_logD = lambda y: -np.log(s).sum(axis=-1)

    elif name == 'norminvcdf':

        f = ndtri
        finv = ndtr
        finv_jac_logD = \
            lambda y: -0.5 * (y ** 2 + np.log(2.0 * np.pi)).sum(axis=-1)
        f_jac_logD = lambda x: -finv_jac_logD(f(x))

    else:
        raise ValueError('unknown bijection: {0}'.format(name))

    return f, finv, f_jac_logD, finv_jac_logD