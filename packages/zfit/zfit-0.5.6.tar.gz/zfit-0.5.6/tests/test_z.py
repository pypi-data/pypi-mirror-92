#  Copyright (c) 2020 zfit

import numpy as np
import tensorflow as tf

from zfit import z
# noinspection PyUnresolvedReferences
from zfit.core.testing import setup_function, teardown_function, tester


def numpy_func(x, a):
    return np.square(x) * a


@z.function
def wrapped_numpy_func(x_tensor, a_tensor):
    result = z.py_function(func=numpy_func, inp=[x_tensor, a_tensor], Tout=tf.float64)
    result = tf.sqrt(result)
    return result


def test_wrapped_func():
    rnd = z.random.uniform(shape=(10,))
    result = wrapped_numpy_func(rnd, z.constant(3.))
    np.testing.assert_allclose(rnd * np.sqrt(3), result)
