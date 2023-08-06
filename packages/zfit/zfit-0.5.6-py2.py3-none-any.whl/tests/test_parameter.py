#  Copyright (c) 2020 zfit
from math import pi, cos

import pytest
import tensorflow as tf
from ordered_set import OrderedSet

import zfit
from zfit import Parameter, z
from zfit.core.parameter import ComposedParameter, ComplexParameter
# noinspection PyUnresolvedReferences
from zfit.core.testing import setup_function, teardown_function, tester
from zfit.util.exception import NameAlreadyTakenError


def test_complex_param():
    real_part = 1.3
    imag_part = 0.3

    # Constant complex
    def complex_value():
        return real_part + imag_part * 1.j

    param1 = ComplexParameter("param1_compl", complex_value, params=None)
    some_value = 3. * param1 ** 2 - 1.2j
    true_value = 3. * complex_value() ** 2 - 1.2j
    assert true_value == pytest.approx(some_value.numpy(), rel=1e-8)
    assert not param1.get_cache_deps()
    # Cartesian complex
    real_part_param = Parameter("real_part_param", real_part)
    imag_part_param = Parameter("imag_part_param", imag_part)
    param2 = ComplexParameter.from_cartesian("param2_compl", real_part_param, imag_part_param)
    part1, part2 = param2.get_cache_deps()
    part1_val, part2_val = [part1.value().numpy(), part2.value().numpy()]
    if part1_val == pytest.approx(real_part):
        assert part2_val == pytest.approx(imag_part)
    elif part2_val == pytest.approx(real_part):
        assert part1_val == pytest.approx(imag_part)
    else:
        assert False, "one of the if or elif should be the case"
    # Polar complex
    mod_val = 1.0
    arg_val = pi / 4.0
    mod_part_param = Parameter("mod_part_param", mod_val)
    arg_part_param = Parameter("arg_part_param", arg_val)
    param3 = ComplexParameter.from_polar("param3_compl", mod_part_param, arg_part_param)
    part1, part2 = param3.get_cache_deps()
    part1_val, part2_val = [part1.value().numpy(), part2.value().numpy()]
    if part1_val == pytest.approx(mod_val):
        assert part2_val == pytest.approx(arg_val)
    elif part1_val == pytest.approx(arg_val):
        assert part2_val == pytest.approx(mod_val)
    else:
        assert False, "one of the if or elif should be the case"

    param4_name = "param4"
    param4 = ComplexParameter.from_polar(param4_name, 4., 2., floating=True)
    deps_param4 = param4.get_cache_deps()
    assert len(deps_param4) == 2
    for dep in deps_param4:
        assert dep.floating
    assert param4.mod.name == param4_name + "_mod"
    assert param4.arg.name == param4_name + "_arg"

    # Test properties (1e-8 is too precise)
    assert real_part == pytest.approx(param1.real.numpy(), rel=1e-6)
    assert imag_part == pytest.approx(param2.imag.numpy(), rel=1e-6)
    assert mod_val == pytest.approx(param3.mod.numpy(), rel=1e-6)
    assert arg_val == pytest.approx(param3.arg.numpy(), rel=1e-6)
    assert cos(arg_val) == pytest.approx(param3.real.numpy(), rel=1e-6)


def test_repr():
    val = 1543
    val2 = 1543 ** 2
    param1 = Parameter('param1', val)
    param2 = zfit.ComposedParameter('comp1', lambda x: x ** 2, params=param1)
    repr_value = repr(param1)
    repr_value2 = repr(param2)
    assert str(val) in repr_value
    assert str(val) in repr_value2

    @z.function
    def tf_call():
        repr_value = repr(param1)
        repr_value2 = repr(param2)
        assert str(val) not in repr_value
        assert str(val2) not in repr_value2
        assert 'graph-node' in repr_value
        assert 'graph-node' in repr_value2

    if zfit.run.get_graph_mode():  # only test if running in graph mode
        tf_call()


def test_composed_param():
    param1 = Parameter('param1', 1.)
    param2 = Parameter('param2', 2.)
    param3 = Parameter('param3', 3., floating=False)
    param4 = Parameter('param4', 4.)  # noqa Needed to make sure it does not only take all params as deps

    def value_fn(p1, p2, p3):
        return z.math.log(3. * p1) * tf.square(p2) - p3

    param_a = ComposedParameter('param_as', value_fn=value_fn, params=(param1, param2, param3))
    param_a2 = ComposedParameter('param_as2', value_fn=value_fn, params={f'p{i}': p
                                                                         for i, p in
                                                                         enumerate((param1, param2, param3))})
    assert param_a2.params['p1'] == param2
    assert isinstance(param_a.get_cache_deps(only_floating=True), OrderedSet)
    assert param_a.get_cache_deps(only_floating=True) == {param1, param2}
    assert param_a.get_cache_deps(only_floating=False) == {param1, param2, param3}
    a_unchanged = value_fn(param1, param2, param3).numpy()
    assert a_unchanged == param_a.numpy()
    assert param2.assign(3.5).numpy()
    a_changed = value_fn(param1, param2, param3).numpy()
    assert a_changed == param_a.numpy()
    assert a_changed != a_unchanged

    print(param_a)

    @z.function
    def print_param(p):
        print(p)

    print_param(param_a)

    # TODO(params): reactivate to check?
    # with pytest.raises(LogicalUndefinedOperationError):
    #     param_a.assign(value=5.)
    # with pytest.raises(LogicalUndefinedOperationError):
    #     param_a.assign(value=5.)


def test_shape_parameter():
    a = Parameter(name='a', value=1)
    assert a.shape.rank == 0


def test_shape_composed_parameter():
    a = Parameter(name='a', value=1)
    b = Parameter(name='b', value=2)

    def compose():
        return tf.square(a) - b

    c = ComposedParameter(name='c', value_fn=compose, dependents=[a, b])
    assert c.shape.rank == 0


# TODO: add test
def test_randomize():
    param1 = zfit.Parameter('param1', 1.0, 0, 2)
    for _ in range(100):
        param1.randomize()
        assert 0 < param1 < 2


def test_floating_behavior():
    param1 = zfit.Parameter('param1', 1.0)
    assert param1.floating


def test_param_limits():
    lower, upper = -4., 3.
    param1 = Parameter('param1', 1., lower_limit=lower, upper_limit=upper)
    param2 = Parameter('param2', 2.)

    assert param1.has_limits
    assert not param2.has_limits

    param1.set_value(upper + 0.5)
    assert upper == param1.value().numpy()
    assert param1.at_limit
    param1.set_value(lower - 1.1)
    assert lower == param1.value().numpy()
    assert param1.at_limit
    param1.set_value(upper - 0.1)
    assert not param1.at_limit

    param2.lower = lower
    param2.set_value(lower - 1.1)
    assert lower == param2.value().numpy()


def test_overloaded_operators():
    param1 = zfit.Parameter('param1', 5)
    param2 = zfit.Parameter('param2', 3)
    param_a = ComposedParameter('param_a', lambda p1: p1 * 4, params=param1)
    param_b = ComposedParameter('param_b', lambda p2: p2, params=param2)
    param_c = param_a * param_b
    assert not isinstance(param_c, zfit.Parameter)
    param_d = ComposedParameter("param_d", lambda pa, pb: pa + pa * pb ** 2, params=[param_a, param_b])
    param_d_val = param_d.numpy()
    assert param_d_val == (param_a + param_a * param_b ** 2).numpy()


# @pytest.mark.skip  # TODO: reactivate, causes segfault
def test_equal_naming():
    param_unique_name = zfit.Parameter('fafdsfds', 5.)
    with pytest.raises(NameAlreadyTakenError):
        param_unique_name2 = zfit.Parameter('fafdsfds', 3.)


# @pytest.mark.skip  # TODO: segfaulting?
def test_set_value():
    value1 = 1.
    value2 = 2.
    value3 = 3.
    value4 = 4.
    param1 = zfit.Parameter(name="param1", value=value1)
    assert param1.numpy() == value1
    with param1.set_value(value2):
        assert param1.numpy() == value2
        param1.set_value(value3)
        assert param1.numpy() == value3
        with param1.set_value(value4):
            assert param1.numpy() == value4
        assert param1.numpy() == value3
    assert param1.numpy() == value1


def test_fixed_param():
    obs = zfit.Space("obs1", (-1, 2))
    sigma = zfit.param.ConstantParameter('const1', 5)
    gauss = zfit.pdf.Gauss(1., sigma, obs=obs)
    mu = gauss.params['mu']
    assert isinstance(mu, zfit.param.ConstantParameter)
    assert isinstance(sigma, zfit.param.ConstantParameter)
    assert not sigma.floating
    assert not sigma.independent
    assert sigma.get_cache_deps() == set()


def test_convert_to_parameter():
    pass  # TODO(Mayou36): add tests


def test_set_values():
    init_values = [1, 2, 3]
    second_values = [5, 6, 7]
    params = [zfit.Parameter(f'param_{i}', val) for i, val in enumerate(init_values)]

    with zfit.param.set_values(params, second_values):
        for param, val in zip(params, second_values):
            assert param.value().numpy() == val

    for param, val in zip(params, init_values):
        assert param.value().numpy() == val

    zfit.param.set_values(params, second_values)
    for param, val in zip(params, second_values):
        assert param.value().numpy() == val

    zfit.param.set_values(params, init_values)
    for param, val in zip(params, init_values):
        assert param.value().numpy() == val
