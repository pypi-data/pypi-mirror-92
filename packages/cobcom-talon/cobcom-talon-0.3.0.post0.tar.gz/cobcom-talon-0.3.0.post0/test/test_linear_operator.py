# -*- coding: utf-8 -*-
import unittest

import numpy as np
import scipy.sparse

import talon
import talon.core

datatype = talon.core.DATATYPE


def get_example_linear_operator(operator_type='reference'):
    i = np.array([0, 3, 1, 2, 0, 1])
    j = np.array([0, 0, 1, 1, 2, 3])
    data = np.array([0, 1, 2, 2, 0, 1], dtype=datatype)
    t = scipy.sparse.coo_matrix((data, (i, j)), dtype=int)
    weights = np.array([1, 2, 1, 4, 5, 7], dtype=datatype)
    w = scipy.sparse.coo_matrix((weights, (i, j)))
    g = np.array([[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]], datatype)
    full_matrix = np.array([[1, 0, 5, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],  # end b0
                            [0, 0, 0, 0],
                            [0, 0, 0, 7],
                            [0, 1, 0, 0],  # end b1
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 4, 0, 0],  # end b2
                            [0, 0, 0, 0],
                            [2, 0, 0, 0],
                            [0, 0, 0, 0]], dtype=datatype)
    lo = talon.operator(g, t, w, operator_type)
    return lo, (g, t, w, full_matrix)


class TestConcatenatedLinearOperator(unittest.TestCase):
    def test_type(self):
        lo, __ = get_example_linear_operator('fast')
        self.assertIsInstance(talon.concatenate((lo, lo), axis=0),
                              talon.core.ConcatenatedLinearOperator)
        self.assertIsInstance(talon.concatenate((lo, lo), axis=1),
                              talon.core.ConcatenatedLinearOperator)

    def test_shape(self):
        lo, __ = get_example_linear_operator('fast')
        reference_shape = lo.shape[0] * 2, lo.shape[1]
        composite = talon.concatenate((lo, lo), axis=0)
        self.assertTupleEqual(composite.shape, reference_shape)

        reference_shape = lo.shape[0], lo.shape[1] * 2
        composite = talon.concatenate((lo, lo), axis=1)
        self.assertTupleEqual(composite.shape, reference_shape)

    def test_instance_creation(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')

        vertical = talon.concatenate((lo, lo), 0)
        gt_vertical = np.concatenate([full_matrix] * 2, 0)
        np.testing.assert_almost_equal(vertical.todense(), gt_vertical)

        horizontal = talon.concatenate((lo, lo), 1)
        gt_horizontal = np.concatenate([full_matrix] * 2, 1)
        np.testing.assert_almost_equal(horizontal.todense(), gt_horizontal)

        with self.assertRaises(ValueError):
            _ = talon.concatenate([])
        with self.assertRaises(ValueError):
            _ = talon.concatenate(())

        with self.assertRaises(ValueError):
            _ = talon.concatenate([lo, lo], 20)

        with self.assertRaises(ValueError):
            _ = talon.concatenate([horizontal, lo], 0)
        with self.assertRaises(ValueError):
            _ = talon.concatenate((vertical, lo), 1)

        with self.assertRaises(TypeError):
            _ = talon.concatenate(1)
        with self.assertRaises(TypeError):
            _ = talon.concatenate((lo, 1))
        with self.assertRaises(TypeError):
            _ = talon.concatenate([lo, 1])

    def test_multiplication_vertical(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[1])

        reference_product = np.concatenate([full_matrix] * 2, axis=0) @ x
        my_product = talon.concatenate((lo, lo), axis=0) @ x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_multiplication_horizontal(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[1])
        twice_x = np.concatenate((x, x))

        numpy_concatenate = np.concatenate([full_matrix] * 2, axis=1)
        talon_concatenate = talon.concatenate((lo, lo), axis=1)

        reference_product = numpy_concatenate @ twice_x
        my_product = talon_concatenate @ twice_x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_data_mask_axis0(self):
        # first operator
        i = np.array([0])
        j = np.array([0])
        data = np.array([1])
        indices = scipy.sparse.coo_matrix((data, (i, j)), shape=(3, 2))
        data = np.array([100.])
        weights = scipy.sparse.coo_matrix((data, (i, j)), shape=(3, 2))
        nb_generators, generators_len = 2, 3
        generators = np.random.rand(generators_len, nb_generators)
        op1 = talon.core.LinearOperator(generators, indices, weights)

        # second operator
        i = np.array([2])
        j = np.array([1])
        data = np.array([1])
        indices = scipy.sparse.coo_matrix((data, (i, j)), shape=(3, 2))
        data = np.array([100.])
        weights = scipy.sparse.coo_matrix((data, (i, j)), shape=(3, 2))
        nb_generators, generators_len = 2, 3
        generators = np.random.rand(generators_len, nb_generators)
        op2 = talon.core.LinearOperator(generators, indices, weights)

        m1 = [1, 1, 0, 0, 0, 0]
        m2 = [0, 0, 0, 0, 1, 1]
        ground_truth_mask = np.concatenate((m1, m2), axis=0)

        conc = talon.concatenate((op1, op2), axis=0)
        np.testing.assert_equal(conc.data_mask, ground_truth_mask)


class TestTransposedConcatenatedLinearOperator(unittest.TestCase):
    def test_shape(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')

        axis = 0
        gt_shape = np.concatenate([full_matrix] * 2, axis).T.shape
        my_shape = talon.concatenate([lo] * 2, axis).T.shape
        self.assertTupleEqual(gt_shape, my_shape)

        axis = 1
        gt_shape = np.concatenate([full_matrix] * 2, axis).T.shape
        my_shape = talon.concatenate([lo] * 2, axis).T.shape
        self.assertTupleEqual(gt_shape, my_shape)

    def test_multiplication_originally_vertical(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[0])
        twice_x = np.concatenate((x, x))

        numpy_concatenated = np.concatenate([full_matrix] * 2, 0)
        reference_product = numpy_concatenated.T @ twice_x

        talon_concatenated = talon.concatenate((lo, lo), axis=0)
        my_product = talon_concatenated.T @ twice_x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_multiplication_originally_horizontal(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[0])

        numpy_concatenated = np.concatenate([full_matrix] * 2, 1)
        reference_product = numpy_concatenated.T @ x

        talon_concatenated = talon.concatenate([lo] * 2, axis=1)
        my_product = talon_concatenated.T @ x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_double_transpose(self):
        lo, _ = get_example_linear_operator('fast')
        concatenated = talon.concatenate([lo] * 2, axis=1)
        self.assertIs(concatenated.T.T, concatenated)


class TestNormalizeAtoms(unittest.TestCase):
    def test_norm(self):
        lo, (g, t, w, full_matrix) = get_example_linear_operator('fast')

        normalized_lo = talon.operator(*talon.normalize(g, t, w))

        expected = np.ones(lo.shape[1])
        computed = np.linalg.norm(normalized_lo.todense(), axis=0)

        np.testing.assert_almost_equal(computed, expected)

    def test_empty_column(self):
        i = np.array([0])
        j = np.array([0])
        data = np.array([1])
        t = scipy.sparse.coo_matrix((data, (i, j)), dtype=int, shape=(2, 2))
        weights = np.array([1.0], dtype=datatype)
        w = scipy.sparse.coo_matrix((weights, (i, j)), shape=(2, 2))
        g = np.array([[1., 0., 0.],
                      [0., 1., 0.],
                      [0., 0., 1.]], datatype)

        with self.assertRaises(ValueError):
            talon.normalize(g, t, w)
