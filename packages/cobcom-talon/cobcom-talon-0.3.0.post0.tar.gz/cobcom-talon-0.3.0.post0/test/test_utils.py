import unittest

import numpy as np
import scipy.sparse as sp

import talon


class TestConcatenateGiw(unittest.TestCase):
    """Test the talon.utils.concatenate_giw function"""

    def test_axes(self):
        with self.assertRaises(ValueError):
            talon.utils.concatenate_giw([1, 2], axis=2)

    def test_compatible_generators(self):
        generators = np.reshape(np.linspace(0, 1, 50), (5, 10))
        indices = sp.coo_matrix(
            ([0, 1, 2, 3, 4], ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4))),
            (6, 11),
            dtype=np.int64,
        )
        weights = sp.coo_matrix(
            (np.linspace(1, 2, 5), ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4))),
            (6, 11),
            dtype=np.float64,
        )

        t1 = (generators, indices, weights)
        t2 = (generators[:, :-1], indices, weights)

        with self.assertRaises(ValueError):
            talon.utils.concatenate_giw([t1, t2])

    def test_simple(self):
        """Test the concatenation using simple products"""

        # Generate GIWs that define the linear operators to concatenate.
        generators_left = np.reshape(np.linspace(0, 1, 50), (5, 10))
        indices_left = sp.coo_matrix(
            ([0, 1, 2, 3, 4], ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4))),
            (6, 11),
            dtype=np.int64,
        )
        weights_left = sp.coo_matrix(
            (np.linspace(1, 2, 5), ((0, 1, 2, 3, 4), (0, 1, 2, 3, 4))),
            (6, 11),
            dtype=np.float64,
        )
        lo_left = talon.operator(
            generators_left, indices_left, weights_left)

        generators_right = np.reshape(np.linspace(0, 1, 30), (3, 10))
        indices_right = sp.coo_matrix(
            ([0, 1, 2], ((2, 3, 4), (0, 1, 2))),
            (6, 11),
            dtype=np.int64,
        )
        weights_right = sp.coo_matrix(
            (np.linspace(2, 3, 3), ((2, 3, 4), (0, 1, 2))),
            (6, 11),
            dtype=np.float64,
        )
        lo_right = talon.operator(
            generators_right, indices_right, weights_right)

        # Along axis 0, the product of the concatenation should be the sum of
        # the individual products.
        giw = talon.utils.concatenate_giw([
            (generators_left, indices_left, weights_left),
            (generators_right, indices_right, weights_right),
        ], axis=0)
        concatenated_lo = talon.operator(*giw)
        x = np.linspace(1, 2, concatenated_lo.shape[1])
        np.testing.assert_array_almost_equal(
            concatenated_lo @ x,
            lo_left @ x[:lo_left.shape[1]] + lo_right @ x[lo_left.shape[1]:],
        )

        # Along axis 1, the product of the concatenation should be the stack of
        # the individual products.
        giw = talon.utils.concatenate_giw([
            (generators_left, indices_left, weights_left),
            (generators_right, indices_right, weights_right),
        ], axis=1)
        concatenated_lo = talon.operator(*giw)
        x = np.linspace(1, 2, concatenated_lo.shape[1])
        np.testing.assert_array_almost_equal(
            concatenated_lo @ x,
            np.hstack((lo_left @ x, lo_right @ x)),
        )


class TestFibonacci(unittest.TestCase):
    def test_shape(self):
        n = np.random.randint(100) + 1
        sphere = talon.utils.directions(n)

        self.assertTupleEqual((n, 3), sphere.shape)

    def test_error(self):
        with self.assertRaises(ValueError):
            talon.utils.directions(-1)

        with self.assertRaises(ValueError):
            talon.utils.directions(0)

    def test_z_coordinate(self):
        n = np.random.randint(100) + 1
        sphere = talon.utils.directions(n)

        self.assertTrue(np.all(sphere[:, 2] > 0))


class TestMaskData(unittest.TestCase):
    def test_zero_out_entries(self):
        i = np.array([0])
        j = np.array([0])
        data = np.array([1])
        indices = sp.coo_matrix((data, (i, j)), shape=(3, 2))
        data = np.array([100.])
        weights = sp.coo_matrix((data, (i, j)), shape=(3, 2))
        nb_generators, generators_len = 2, 3
        generators = np.random.rand(generators_len, nb_generators)
        lop = talon.core.LinearOperator(generators, indices, weights)

        mask = np.array([True, True, False, False, False, False], dtype=bool)
        np.testing.assert_equal(mask, lop.data_mask)

        data = np.array([1, 2, 3, 4, 5, 6])

        masked = talon.utils.mask_data(data, lop)
        expected = np.array([1, 2, 0, 0, 0, 0])

        np.testing.assert_equal(masked, expected)


class TestCheckPattern(unittest.TestCase):
    def test_bad_weights(self):
        indices = sp.coo_matrix((10, 10), np.int)
        bad_weights = sp.coo_matrix(([1.0], ((1,), (1,))), shape=(10, 10))

        self.assertRaises(
            ValueError, talon.utils.check_pattern_iw, indices, bad_weights)
