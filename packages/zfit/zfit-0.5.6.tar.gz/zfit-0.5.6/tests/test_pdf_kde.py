#  Copyright (c) 2020 zfit

import numpy as np
import pytest

import zfit
import zfit.models.dist_tfp
import zfit.models.kde


# noinspection PyUnresolvedReferences
from zfit.core.testing import setup_function, teardown_function, tester

@pytest.mark.skip()  # copy not yet implemented
def test_copy_kde():
    size = 500
    data = np.random.normal(size=size, loc=2, scale=3)

    limits = (-15, 5)
    obs = zfit.Space("obs1", limits=limits)
    kde_adaptive = zfit.models.kde.GaussianKDE1DimV1(data=data, bandwidth='adaptiveV1',
                                                     obs=obs,
                                                     truncate=False)
    kde_adaptive.copy()


def test_simple_kde():
    expected_integral = 5 / 6
    h = zfit.Parameter("h", 0.9)

    size = 5000
    data = np.random.normal(size=size, loc=2, scale=3)

    limits = (-15, 5)
    obs = zfit.Space("obs1", limits=limits)
    data_truncated = obs.filter(data)
    kde = zfit.models.kde.GaussianKDE1DimV1(data=data, bandwidth=h, obs=obs,
                                            truncate=False)
    kde_adaptive = zfit.models.kde.GaussianKDE1DimV1(data=data, bandwidth='adaptiveV1',
                                                     obs=obs,
                                                     truncate=False)
    kde_silverman = zfit.models.kde.GaussianKDE1DimV1(data=data, bandwidth='silverman',
                                                      obs=obs,
                                                      truncate=False)
    kde_adaptive_trunc = zfit.models.kde.GaussianKDE1DimV1(data=data_truncated, bandwidth='adaptiveV1',
                                                           obs=obs,
                                                           truncate=True)

    integral = kde.integrate(limits=limits, norm_range=False)
    integral_trunc = kde_adaptive_trunc.integrate(limits=limits, norm_range=False)
    integral_adaptive = kde_adaptive.integrate(limits=limits, norm_range=False)
    integral_silverman = kde_silverman.integrate(limits=limits, norm_range=False)

    rel_tol = 0.04
    assert zfit.run(integral_trunc) == pytest.approx(1., rel=rel_tol)
    assert zfit.run(integral) == pytest.approx(expected_integral, rel=rel_tol)
    assert zfit.run(integral_adaptive) == pytest.approx(expected_integral, rel=rel_tol)
    assert zfit.run(integral_silverman) == pytest.approx(expected_integral, rel=rel_tol)

    sample = kde_adaptive.sample(1000)
    sample2 = kde_adaptive_trunc.sample(1000)
    assert sample.nevents == 1000
    assert sample2.nevents == 1000
