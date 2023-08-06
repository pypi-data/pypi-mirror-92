from unittest import TestCase

import numpy as  np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsmr

import talon


class TestSolvers(TestCase):

    def test_lsmr_dense(self):
        """Test the scipy LSMR solver using dense talon linear operators"""

        # Dense matrix.
        dense_matrix = np.random.randn(120, 10)
        x = np.random.randn(10)
        y = dense_matrix @ x

        numpy_weights = np.random.randn(10, 10)
        weights = coo_matrix(numpy_weights)

        # The generators are obtained by slicing the matrix in blocks of rows.
        generators = np.zeros((1, 12))
        for i in range(0, 120, 12):
            generators = np.vstack((generators, dense_matrix[i:i + 12, :].T))
        generators[1:, :] /= numpy_weights.ravel()[:, None]

        # The indices are all unique because each generator is used once. Note
        # that the first generator is not used.
        indices = coo_matrix(np.arange(100).reshape((10, 10)) + 1)

        linear_operator = talon.operator(generators, indices, weights)

        # Solving with the dense operator or the talon one should yield the
        # same result.
        talon_x, *_ = lsmr(linear_operator, y)
        numpy_x, *_ = lsmr(dense_matrix, y)
        np.testing.assert_array_almost_equal(talon_x, numpy_x)
