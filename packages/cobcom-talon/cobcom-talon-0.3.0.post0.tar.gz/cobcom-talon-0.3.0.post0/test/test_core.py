from unittest import TestCase

import numpy as np
from scipy.sparse import coo_matrix

from talon.core import LinearOperator


class TestLinearOperator(TestCase):
    def __init__(self, *args):
        """Testing for linear operators

        This testing class tests that linear operators, and in particular their
        __matmul__ method, are correct. It is meant to be subclassed for each
        implementation of a linear operator.

        Note that this test class assumes that the linear operator is
        initialized using a generator, indices, and weights triplet. If this is
        not the case, it cannot be used to test the operator.

        """

        super().__init__(*args)

        # Define the test data at initialization so that all subclasses use the
        # same data even if it is generated randomly.

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
        self.dense_matrix_data = (
            dense_matrix, generators, indices, weights, x, y)

        # Sparse matrix.
        generators = np.random.randn(2, 24)
        rows = [0, 19]
        columns = [0, 9]
        data = [1, 0]
        indices = coo_matrix((data, (rows, columns)), shape=(20, 10))
        weights = coo_matrix(([1.0, 1.0], (rows, columns)), shape=(20, 10))
        sparse_matrix = np.zeros((480, 10))
        sparse_matrix[0:24, 0] = generators[1]
        sparse_matrix[456:, 9] = generators[0]
        x = np.random.randn(10)
        y = sparse_matrix @ x
        self.sparse_matrix_data = (
            sparse_matrix, generators, indices, weights, x, y)

    @property
    def linear_operator(self):
        return LinearOperator

    def test_init_assert(self):
        """Test the use of bad inputs in the __init__ method."""

        generators = np.empty((0, 10))
        indices = coo_matrix((10, 10), np.int)
        weights = coo_matrix((10, 10), np.float)

        # The generators must be a numpy array of np.float64.
        self.assertRaises(
            TypeError, self.linear_operator, [], indices, weights)
        self.assertRaises(
            TypeError, self.linear_operator, generators.astype(np.float32),
            indices, weights)

        # The indices must be a coo_matrix.
        self.assertRaises(
            TypeError, self.linear_operator, generators, [], weights)

        # The weights must be a coo_matrix of np.float64.
        self.assertRaises(
            TypeError, self.linear_operator, generators, indices, [])
        self.assertRaises(
            TypeError, self.linear_operator, generators, indices,
            weights.astype(np.float32))

        # The indices and the weights must have the same shape.
        bad_weights = coo_matrix((11, 10), np.float)
        self.assertRaises(
            ValueError, self.linear_operator, generators, indices, bad_weights)

    def test_properties_dense_matrix(self):
        """Test the properties using a dense matrix."""

        matrix, generators, indices, weights, x, y = self.dense_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)

        self.assertEqual(linear_operator.nb_data, indices.shape[0])
        self.assertEqual(linear_operator.nb_atoms, indices.shape[1])
        self.assertEqual(linear_operator.nb_generators, len(generators))
        self.assertTupleEqual(linear_operator.shape, matrix.shape)

    def test_matmul_assert(self):
        """Test the use of bad inputs in the __matmul__ method."""

        generators = np.ones((1, 16))
        indices = coo_matrix((10, 10), np.int)
        weights = coo_matrix((10, 10), np.float)
        linear_operator = self.linear_operator(generators, indices, weights)

        # The vector must be 1D.
        self.assertRaises(
            ValueError, linear_operator.__matmul__, np.ones((10, 10)))

        # The shape must match the second dimension of the linear operator.
        self.assertRaises(
            ValueError, linear_operator.__matmul__, np.ones(12))

    def test_matmul_all_zeros(self):
        """Test the __matmul__ method with an all zero linear operator"""

        # Build a linear operator of the class being tested using empty
        # matrices.
        generators = np.empty((0, 8))
        indices = coo_matrix((10, 10), np.int)
        weights = coo_matrix((10, 10), np.float)
        linear_operator = self.linear_operator(generators, indices, weights)

        self.assertTupleEqual(linear_operator.shape, (80, 10))

        # The product with any x should always be 0.
        y = linear_operator @ np.zeros((10,))
        np.testing.assert_array_almost_equal(y, np.zeros((80,)))

    def test_matmul_dense_matrix(self):
        """Test the __matmul__ method with a dense linear operator."""

        matrix, generators, indices, weights, x, _ = self.dense_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)

        self.assertTupleEqual(linear_operator.shape, (120, 10))

        # The product using the dense matrix and the linear operator should
        # be identical.
        dense_y = matrix @ x
        y = linear_operator @ x
        np.testing.assert_array_almost_equal(dense_y, y, 3)

    def test_matmul_sparse_matrix(self):
        """Test the __matmul__ method with a sparse linear operator."""

        matrix, generators, indices, weights, x, _ = self.sparse_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)

        self.assertTupleEqual(linear_operator.shape, (480, 10))

        # The product using the dense matrix and the linear operator should
        # be identical.
        dense_y = matrix @ x
        y = linear_operator @ x
        np.testing.assert_array_almost_equal(dense_y, y, 3)

    def test_to_dense(self):
        """Test the todense method."""

        # With a dense matrix.
        matrix, generators, indices, weights, x, _ = self.dense_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)
        np.testing.assert_array_almost_equal(linear_operator.todense(), matrix)
        np.testing.assert_array_almost_equal(
            linear_operator.T.todense(), matrix.T)

        # With a sparse matrix.
        matrix, generators, indices, weights, x, _ = self.sparse_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)
        np.testing.assert_array_almost_equal(linear_operator.todense(), matrix)
        np.testing.assert_array_almost_equal(
            linear_operator.T.todense(), matrix.T)

    def test_transpose_dense_matrix(self):
        """Test the transpose method with a dense linear operator."""

        matrix, generators, indices, weights, _, y = self.dense_matrix_data
        linear_operator = self.linear_operator(generators, indices, weights)
        transposed_linear_operator = linear_operator.T

        self.assertTupleEqual(transposed_linear_operator.shape, (10, 120))

        # The product using the dense matrix and the linear operator should
        # be identical.
        dense_x = matrix.T @ y
        x = transposed_linear_operator @ y
        np.testing.assert_array_almost_equal(dense_x, x, 3)

        # The transpose of the transpose is the original operator.
        self.assertEqual(linear_operator, transposed_linear_operator.T)


class TestDataMask(TestCase):
    def test_create_data_mask(self):
        i = np.array([0])
        j = np.array([0])

        data = np.array([1])
        indices = coo_matrix((data, (i, j)), shape=(2, 2))

        data = np.array([100.])
        weights = coo_matrix((data, (i, j)), shape=(2, 2))

        nb_generators, generators_len = 2, 3
        generators = np.random.rand(generators_len, nb_generators)

        lop = LinearOperator(generators, indices, weights)

        ground_truth_mask = np.array([1, 1, 0, 0], dtype=bool)

        np.testing.assert_equal(lop.data_mask, ground_truth_mask)
