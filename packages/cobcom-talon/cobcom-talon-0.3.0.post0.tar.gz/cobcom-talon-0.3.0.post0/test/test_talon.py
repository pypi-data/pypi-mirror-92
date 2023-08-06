import unittest

import numpy as np
import scipy.sparse

import talon
import talon.core
import talon.fast


class TestOperator(unittest.TestCase):
    """Test the talon.operator function"""

    def test_type(self):
        """Test the type parameter"""

        dtype = talon.core.DATATYPE
        nb_rows, nb_columns, nb_generators = 100, 200, 100

        sparse = scipy.sparse.random(
            nb_rows, nb_columns, density=0.1, dtype=dtype)
        data = sparse.data
        indices = np.round(data / (data.max() + 1) * nb_generators).astype(int)

        indices_of_generators = scipy.sparse.coo_matrix(
            (indices, (sparse.row, sparse.col)), dtype=int)

        weights = scipy.sparse.coo_matrix(
            (data, (sparse.row, sparse.col)), dtype=dtype)

        generators = np.random.randn(nb_generators, 20)

        # The default is a fast operator.
        operator = talon.operator(generators, indices_of_generators, weights)
        self.assertIsInstance(operator, talon.fast.LinearOperator)

        # We can explicitly ask for a fast operator.
        operator = talon.operator(generators, indices_of_generators,
                                  weights, 'fast')
        self.assertIsInstance(operator, talon.fast.LinearOperator)

        # We can ask for the reference operator.
        operator = talon.operator(generators, indices_of_generators,
                                  weights, 'reference')
        self.assertIsInstance(operator, talon.core.LinearOperator)

        # Fails on invalid type.
        self.assertRaises(ValueError, talon.operator, generators,
                          indices_of_generators, weights, 'nonsense')


class TestZeros(unittest.TestCase):
    """Test the talon.zeros function"""

    def test_simple(self):
        """Test normal usage"""

        shape = (100000, 1000)
        lo = talon.zeros(shape)

        # Test the shape of the linear operator.
        self.assertTupleEqual(shape, lo.shape)

        # The product should always be zero.
        x = np.random.randn(lo.shape[1])
        np.testing.assert_array_almost_equal(lo @ x, np.zeros(lo.shape[0]))

        # The transpose is also all zeros.
        b = np.random.randn(lo.shape[0])
        np.testing.assert_array_almost_equal(lo.T @ b, np.zeros(lo.shape[1]))
