#  Copyright (c) 2020 zfit

from typing import Dict, Type

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import zfit.core.basepdf
import zfit.models.dist_tfp
import zfit.settings
from zfit import z
from zfit.core.interfaces import ZfitParameter
from zfit.core.space import Space, ANY_UPPER, MultiSpace
from zfit.core.parameter import Parameter
# noinspection PyUnresolvedReferences
from zfit.core.testing import setup_function, teardown_function, tester
from zfit.models.dist_tfp import Gauss
from zfit.models.special import SimplePDF
# from zfit.z import
from zfit.util import ztyping
from zfit.util.exception import AlreadyExtendedPDFError, BreakingAPIChangeError, SpaceIncompatibleError, \
    CoordinatesUnderdefinedError, ObsIncompatibleError

test_values = np.array([3., 11.3, -0.2, -7.82])

mu_true = 1.4
sigma_true = 1.8
low, high = -4.3, 1.9

obs1 = zfit.Space('obs1', (low, high))


def create_gauss1(nameadd=""):
    mu = Parameter("mu" + nameadd, mu_true, mu_true - 2., mu_true + 7.)
    sigma = Parameter("sigma" + nameadd, sigma_true, sigma_true - 10., sigma_true + 5.)

    gauss_params1 = Gauss(mu=mu, sigma=sigma, obs=obs1, name="gauss_params1")
    return gauss_params1


def create_mu_sigma_true_params():
    mu_true_param = zfit.Parameter('mu_true', mu_true)
    sigma_true_param = zfit.Parameter('sigma_true', sigma_true)
    return mu_true_param, sigma_true_param


class TmpGaussian(zfit.pdf.BasePDF):

    def __init__(self, obs: ztyping.ObsTypeInput, mu, sigma, params: Dict[str, ZfitParameter] = None,
                 dtype: Type = zfit.ztypes.float,
                 name: str = "BasePDF", **kwargs):
        params = {'mu': mu, 'sigma': sigma}
        super().__init__(obs, params, dtype, name, **kwargs)

    def _unnormalized_pdf(self, x):
        x = x.unstack_x()
        mu = self.params['mu']
        sigma = self.params['sigma']

        return tf.exp((-(x - mu) ** 2) / (
            2 * sigma ** 2))  # non-normalized gaussian


def true_gaussian_unnorm_func(x):
    return np.exp(- (x - mu_true) ** 2 / (2 * sigma_true ** 2))


def true_gaussian_grad(x):
    grad_mu = -0.199471140200716 * (2 * mu_true - 2 * x) * np.exp(
        -(-mu_true + x) ** 2 / (2 * sigma_true ** 2)) / sigma_true ** 3
    grad_sigma = -0.398942280401433 * np.exp(
        -(-mu_true + x) ** 2 / (2 * sigma_true ** 2)) / sigma_true ** 2 + 0.398942280401433 * (
                     -mu_true + x) ** 2 * np.exp(-(-mu_true + x) ** 2 / (2 * sigma_true ** 2)) / sigma_true ** 4
    return np.array((grad_mu, grad_sigma)).transpose()


def create_mu_sigma_2(nameadd=""):
    mu2 = Parameter("mu2" + nameadd, mu_true, mu_true - 2., mu_true + 7.)
    sigma2 = Parameter("sigma2" + nameadd, sigma_true, sigma_true - 10., sigma_true + 5.)
    return mu2, sigma2


def create_wrapped_gauss(nameadd=""):
    mu2, sigma2 = create_mu_sigma_2(nameadd)
    gauss_params = dict(loc=mu2, scale=sigma2)
    tf_gauss = tfp.distributions.Normal
    return zfit.models.dist_tfp.WrapDistribution(tf_gauss, dist_params=gauss_params, obs=obs1, name="tf_gauss1")


def create_gauss3(nameadd=""):
    mu3 = Parameter("mu3" + nameadd, mu_true, mu_true - 2., mu_true + 7.)
    sigma3 = Parameter("sigma3" + nameadd, sigma_true, sigma_true - 10., sigma_true + 5.)
    gauss3 = zfit.pdf.Gauss(mu=mu3, sigma=sigma3, obs=obs1)
    return gauss3


def create_test_gauss1():
    mu, sigma = create_mu_sigma_true_params()
    return TmpGaussian(name="test_gauss1", mu=mu, sigma=sigma, obs=obs1)


def create_wrapped_normal1(nameadd=""):
    mu2, sigma2 = create_mu_sigma_2(nameadd)
    return Gauss(mu=mu2, sigma=sigma2, obs=obs1, name='wrapped_normal1')


def create_gaussian_dists():
    return [create_test_gauss1(), create_gauss1("dists")]


# starting tests
# ===============================
@pytest.mark.skip  # TODO: should we have gradients in PDFs? Nope, remove
def test_gradient():
    gauss3 = create_gauss3()
    random_vals = np.random.normal(4., 2., size=5)
    tensor_grad = gauss3.gradients(x=random_vals, params=['mu', 'sigma'], norm_range=(-np.infty, np.infty))
    random_vals_eval = tensor_grad.numpy()
    np.testing.assert_allclose(random_vals_eval, true_gaussian_grad(random_vals), rtol=1e-3)


def test_input_space():
    gauss3 = create_gauss3()
    space = zfit.Space('nonexisting_obs', (-3, 5))
    with pytest.raises(ObsIncompatibleError):
        gauss3.set_norm_range(space)


def test_func():
    test_values = np.array([3., 11.3, -0.2, -7.82])
    test_values = zfit.Data.from_numpy(obs=obs1, array=test_values)

    gauss_params1 = create_gauss1()

    limits = (-15, 5)

    gauss_func = gauss_params1.as_func(norm_range=limits)
    vals = gauss_func.func(test_values)
    vals_pdf = gauss_params1.pdf(x=test_values, norm_range=limits)
    vals, vals_pdf = [vals.numpy(), vals_pdf.numpy()]
    np.testing.assert_allclose(vals_pdf, vals, rtol=1e-3)  # better assertion?


@pytest.mark.parametrize('pdf_factory',
                         [lambda: create_gaussian_dists()[0],
                          lambda: create_gaussian_dists()[1],
                          create_wrapped_gauss,
                          create_wrapped_normal1])
def test_normalization(pdf_factory):
    test_yield = 1524.3
    dist = pdf_factory()
    samples = tf.cast(np.random.uniform(low=low, high=high, size=100000), dtype=tf.float64)
    small_samples = tf.cast(np.random.uniform(low=low, high=high, size=10), dtype=tf.float64)
    with dist.set_norm_range(Space(obs1, limits=(low, high))):
        probs = dist.pdf(samples)
        probs_small = dist.pdf(small_samples)
        log_probs = dist.log_pdf(small_samples)
        probs, log_probs = probs.numpy(), log_probs.numpy()
        probs = np.average(probs) * (high - low)
        assert probs == pytest.approx(1., rel=0.05)
        assert log_probs == pytest.approx(tf.math.log(probs_small).numpy(), rel=0.05)
        dist = dist.create_extended(z.constant(test_yield))
        probs = dist.pdf(samples)
        probs_extended = dist.ext_pdf(samples)
        result = probs.numpy()
        result = np.average(result) * (high - low)
        result_ext = np.average(probs_extended) * (high - low)
        assert result == pytest.approx(1, rel=0.05)
        assert result_ext == pytest.approx(test_yield, rel=0.05)


@pytest.mark.parametrize('gauss_factory', [create_gauss1, create_test_gauss1])
def test_sampling_simple(gauss_factory):
    gauss = gauss_factory()
    n_draws = 1000
    sample_tensor = gauss.sample(n=n_draws, limits=(low, high))
    sampled_from_gauss1 = sample_tensor.numpy()
    assert max(sampled_from_gauss1[:, 0]) <= high
    assert min(sampled_from_gauss1[:, 0]) >= low
    assert n_draws == len(sampled_from_gauss1[:, 0])
    if gauss.params:
        mu_true1 = gauss.params['mu'].numpy()
        sigma_true1 = gauss.params['sigma'].numpy()
    else:
        mu_true1 = mu_true
        sigma_true1 = sigma_true
    sampled_gauss1_full = gauss.sample(n=10000,
                                       limits=(mu_true1 - abs(sigma_true1) * 3, mu_true1 + abs(sigma_true1) * 3))
    sampled_gauss1_full = sampled_gauss1_full.numpy()
    mu_sampled = np.mean(sampled_gauss1_full)
    sigma_sampled = np.std(sampled_gauss1_full)
    assert mu_sampled == pytest.approx(mu_true1, rel=0.07)
    assert sigma_sampled == pytest.approx(sigma_true1, rel=0.07)

# @pytest.mark.skip  # bug fixed upsteams TODO(ASAP)
def test_sampling_multiple_limits():
    gauss_params1 = create_gauss1()
    n_draws = 1000
    low1, up1 = -1, 0
    lower_interval = zfit.Space(obs=obs1, limits=(low1, up1))
    low2, up2 = 1, 2
    upper_interval = zfit.Space(obs=obs1, limits=(low2, up2))
    sample_tensor = gauss_params1.sample(n=n_draws, limits=lower_interval + upper_interval)
    sampled_from_gauss1 = sample_tensor.numpy()
    between_samples = np.logical_and(sampled_from_gauss1 < up1, sampled_from_gauss1 > low2)
    assert not any(between_samples)
    assert max(sampled_from_gauss1[:, 0]) <= up2
    assert min(sampled_from_gauss1[:, 0]) >= low1
    assert n_draws == len(sampled_from_gauss1[:, 0])

    mu_true = gauss_params1.params['mu'].numpy()
    sigma_true = gauss_params1.params['sigma'].numpy()
    low1, up1 = mu_true - abs(sigma_true) * 4, mu_true
    lower_interval = zfit.Space(obs=obs1, limits=(low1, up1))
    low2, up2 = mu_true, mu_true + abs(sigma_true) * 4
    upper_interval = zfit.Space(obs=obs1, limits=(low2, up2))
    one_interval = zfit.Space(obs=obs1, limits=(low1, up2))

    sample_tensor5 = gauss_params1.sample(n=10000, limits=lower_interval + upper_interval)
    sampled_gauss1_full = sample_tensor5.numpy()
    mu_sampled = np.mean(sampled_gauss1_full)
    sigma_sampled = np.std(sampled_gauss1_full)
    assert mu_sampled == pytest.approx(mu_true, rel=0.07)
    assert sigma_sampled == pytest.approx(sigma_true, rel=0.07)


def test_analytic_sampling():
    class SampleGauss(TmpGaussian):
        pass

    SampleGauss.register_analytic_integral(func=lambda limits, params, model: 2 * limits.upper[0][0],
                                           limits=Space(limits=(-float("inf"), ANY_UPPER),
                                                        axes=(0,)))  # DUMMY!
    SampleGauss.register_inverse_analytic_integral(func=lambda x, params: x + 1000.)

    mu, sigma = create_mu_sigma_true_params()
    gauss1 = SampleGauss(obs=obs1, mu=mu, sigma=sigma)
    sample = gauss1.sample(n=10000, limits=(2., 5.))
    sample.set_data_range((1002, 1005))

    sample = sample.numpy()

    assert 1004. <= min(sample[0])
    assert 10010. >= max(sample[0])


def test_multiple_limits():
    gauss_params1 = create_gauss1()
    dims = (0,)
    simple_limits = (-3.2, 9.1)
    multiple_limits_lower = ((-3.2,), (1.1,), (2.1,))
    multiple_limits_upper = ((1.1,), (2.1,), (9.1,))

    multiple_limits_range = MultiSpace(
        [Space(limits=(low, up), axes=dims) for low, up in zip(multiple_limits_lower, multiple_limits_upper)])
    integral_simp = gauss_params1.integrate(limits=simple_limits, norm_range=False)
    integral_mult = gauss_params1.integrate(limits=multiple_limits_range, norm_range=False)
    integral_simp_num = gauss_params1.numeric_integrate(limits=simple_limits, norm_range=False)
    integral_mult_num = gauss_params1.numeric_integrate(limits=multiple_limits_range, norm_range=False)

    integral_simp, integral_mult = [integral_simp.numpy(), integral_mult.numpy()]
    integral_simp_num, integral_mult_num = [integral_simp_num.numpy(), integral_mult_num.numpy()]
    assert integral_simp == pytest.approx(integral_mult, rel=1e-2)  # big tolerance as mc is used
    assert integral_simp == pytest.approx(integral_simp_num, rel=1e-2)  # big tolerance as mc is used
    assert integral_simp_num == pytest.approx(integral_mult_num, rel=1e-2)  # big tolerance as mc is used


def test_copy():
    gauss_params1 = create_gauss1()
    new_gauss = gauss_params1.copy()
    assert new_gauss == gauss_params1
    assert new_gauss is not gauss_params1


def test_set_yield():
    gauss_params1 = create_gauss1()
    assert not gauss_params1.is_extended
    gauss_params1._set_yield(10)
    assert gauss_params1.is_extended
    with pytest.raises(AlreadyExtendedPDFError):
        gauss_params1._set_yield(15)

    with pytest.raises(BreakingAPIChangeError):
        gauss_params1._set_yield(None)

def test_projection_pdf():
    x = zfit.Space("x", limits=(-1, 1))
    y = zfit.Space("y", limits=(-1, 1))

    def correlated_func(self, x):
        x, y = x.unstack_x()
        value = (((x - y ** 3) ** 2) + 0.1)
        return value

    def correlated_func_integrate_x(y, limits):
        lower, upper = limits.rect_limits

        def integ(x, y):
            return 0.333333333333333 * x ** 3 - 1.0 * x ** 2 * y ** 3 + x * (1.0 * y ** 6 + 0.1)

        return integ(y, upper) - integ(y, lower)

    def correlated_func_integrate_y(x, limits):
        lower, upper = limits.rect_limits

        def integ(x, y):
            return -0.5 * x * y ** 4 + 0.142857142857143 * y ** 7 + y * (1.0 * x ** 2 + 0.1)

        return (integ(x, upper) - integ(x, lower))[0]

    obs = x * y
    gauss_xy = SimplePDF(func=correlated_func, obs=obs)
    assert gauss_xy.create_projection_pdf(limits_to_integrate=y).norm_range == x
    proj_pdf = gauss_xy.create_projection_pdf(limits_to_integrate=y)
    test_values = np.array([-0.95603563, -0.84636306, -0.83895759, 2.62608006, 1.02336499,
                            -0.99631608, -1.22185623, 0.83838586, 2.77894762, -2.48259488,
                            1.5440374, 0.1109899, 0.20873491, -2.45271623, 2.04510553,
                            0.31566277, -1.55696965, 0.36304538, 0.77765786, 3.92630088])
    true_probs = correlated_func_integrate_y(test_values, y) / gauss_xy.integrate(limits=obs, norm_range=False)
    probs = proj_pdf.pdf(x=test_values)
    probs = probs.numpy()
    np.testing.assert_allclose(probs, true_probs, rtol=1e-3)  # MC normalization
