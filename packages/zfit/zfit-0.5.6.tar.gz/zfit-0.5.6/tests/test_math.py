#  Copyright (c) 2020 zfit
import numpy as np
import pytest
import scipy.stats

import zfit
from zfit import z
# noinspection PyUnresolvedReferences
from zfit.core.testing import setup_function, teardown_function, tester
from zfit.z.math import numerical_gradient, autodiff_gradient, numerical_hessian, autodiff_hessian


def test_numerical_gradient():
    param1 = zfit.Parameter('param1', 4.)
    param2 = zfit.Parameter('param2', 5.)
    param3 = zfit.Parameter('param3', 2.)

    def func1():
        return param1 * param2 ** 2 + param3 ** param1

    num_gradients = numerical_gradient(func1, params=[param1, param2, param3])
    tf_gradients = autodiff_gradient(func1, params=[param1, param2, param3])
    np.testing.assert_allclose(num_gradients, tf_gradients)


@pytest.mark.parametrize('graph', [False, True])
def test_numerical_hessian(graph):
    param1 = zfit.Parameter('param1', 4.)
    param2 = zfit.Parameter('param2', 5.)
    param3 = zfit.Parameter('param3', 2.)

    def func1():
        return param1 * param2 ** 2 + param3 ** param1

    def create_derivatives(func1, params):
        num_hessian_diag = numerical_hessian(func1, params=params, hessian='diag')
        num_hessian = numerical_hessian(func1, params=params)
        tf_hessian_diag = autodiff_hessian(func1, params=params, hessian='diag')
        tf_hessian = autodiff_hessian(func1, params=params)
        return num_hessian, num_hessian_diag, tf_hessian, tf_hessian_diag

    params = [param1, param2, param3]
    if graph:
        create_derivatives = z.function(create_derivatives)
    num_hessian, num_hessian_diag, tf_hessian, tf_hessian_diag = create_derivatives(func1, params)
    np.testing.assert_allclose(num_hessian, tf_hessian, rtol=1e-4, atol=1e-10)
    tf_hessian_diag_from_hessian = [tf_hessian[i, i] for i in range(len(params))]
    np.testing.assert_allclose(tf_hessian_diag_from_hessian, tf_hessian_diag, rtol=1e-4, atol=1e-10)
    np.testing.assert_allclose(num_hessian_diag, tf_hessian_diag, rtol=1e-4, atol=1e-10)


def test_reduce_geometric_mean():
    rnd1 = np.random.poisson(1000, size=(54, 14, 3)).astype(np.float64)
    gmean_np = scipy.stats.mstats.gmean(rnd1, axis=None)
    gmea_z = z.math.reduce_geometric_mean(rnd1)
    np.testing.assert_allclose(gmea_z, gmean_np)
