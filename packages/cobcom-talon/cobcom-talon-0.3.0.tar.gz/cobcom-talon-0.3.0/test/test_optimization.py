# -*- coding: utf-8 -*-
import pickle
import unittest

import numpy as np
import scipy.optimize

import talon

datatype = talon.core.DATATYPE


class TestRegularizationTemplate(unittest.TestCase):
    def test_init_checks(self):
        with self.assertRaises(TypeError):
            talon.optimization.RegularizationTerm(
                regularization_parameter='Hello world!')

        with self.assertRaises(ValueError):
            talon.optimization.RegularizationTerm(
                regularization_parameter=-5)

    def test_no_regularization(self):
        correct_type = talon.optimization.NoRegularization
        regterm1 = talon.regularization()
        regterm2 = talon.regularization(non_negativity=False)
        self.assertIsInstance(regterm1, correct_type)
        self.assertIsInstance(regterm2, correct_type)
        self.assertIsNone(regterm1.groups)
        self.assertEqual(regterm1.non_negativity, False)
        self.assertEqual(regterm1.regularization_parameter, 0.0)
        self.assertIsNone(regterm1.weights)

    def test_non_negativity(self):
        correct_type = talon.optimization.NonNegativity
        regterm = talon.regularization(non_negativity=True)
        self.assertIsInstance(regterm, correct_type)
        self.assertIsNone(regterm.groups)
        self.assertEqual(regterm.non_negativity, True)
        self.assertEqual(regterm.regularization_parameter, 0.0)
        self.assertIsNone(regterm.weights)

    def test_structured_sparsity(self):
        correct_type = talon.optimization.StructuredSparsity
        non_negativity = False
        groups = [1.0]
        weights = [1.0]
        my_lambda = 1.0
        regterm = talon.regularization(non_negativity=non_negativity,
                                       groups=groups,
                                       weights=weights,
                                       regularization_parameter=my_lambda)
        self.assertIsInstance(regterm, correct_type)
        self.assertEqual(regterm.regularization_parameter, my_lambda)
        self.assertEqual(regterm.non_negativity, non_negativity)
        np.testing.assert_almost_equal(regterm.groups, groups)
        np.testing.assert_almost_equal(regterm.weights, weights)

        with self.assertRaises(ValueError):
            talon.regularization(non_negativity=False,
                                 groups=[1.0],
                                 weights=[1.0, 2.0],
                                 regularization_parameter=1.0)
        with self.assertRaises(ValueError):
            talon.regularization(non_negativity=False,
                                 groups=[1.0],
                                 weights=[1.0],
                                 regularization_parameter=-1.0)

        # check that by annihilating the regularisation parameter it yields the
        # correct regularisation object
        r = talon.regularization(non_negativity=False,
                                 groups=[1.0],
                                 weights=[1.0],
                                 regularization_parameter=0)
        self.assertIsInstance(r, talon.optimization.NoRegularization)

    def test_non_negative_structured_sparsity(self):
        correct_type = talon.optimization.NonNegativeStructuredSparsity
        non_negativity = True
        groups = [1.0]
        weights = [1.0]
        my_lambda = 1.0
        regterm = talon.regularization(non_negativity=non_negativity,
                                       groups=groups,
                                       weights=weights,
                                       regularization_parameter=my_lambda)
        self.assertIsInstance(regterm, correct_type)
        self.assertEqual(regterm.regularization_parameter, my_lambda)
        self.assertEqual(regterm.non_negativity, non_negativity)
        np.testing.assert_almost_equal(regterm.groups, groups)
        np.testing.assert_almost_equal(regterm.weights, weights)


class TestPickling(unittest.TestCase):
    def test_dump_and_reload(self):
        x = np.array([0.01, 0.05, 3., -4.])
        groups = [[0, 1], [2, 3]]
        weights = np.array([1.0, 2.])
        regterm = talon.optimization.NonNegativeStructuredSparsity(
            1.0, groups, weights)

        saved = pickle.dumps(regterm)
        reloaded = pickle.loads(saved)

        self.assertEqual(regterm(x), reloaded(x))
        self.assertIsInstance(reloaded, type(regterm))
        self.assertEqual(regterm.non_negativity, reloaded.non_negativity)
        self.assertEqual(regterm.regularization_parameter,
                         reloaded.regularization_parameter)
        np.testing.assert_almost_equal(regterm.groups, reloaded.groups)
        np.testing.assert_almost_equal(regterm.weights, reloaded.weights)


class TestNonNegativity(unittest.TestCase):
    def test_eval(self):
        x = np.random.rand(np.random.randint(100) + 2)
        regterm = talon.optimization.NonNegativity()
        eval_regterm_positive = regterm._eval(x)
        eval_regterm_negative = regterm._eval(-x)
        self.assertAlmostEqual(eval_regterm_positive, 0.0)
        self.assertAlmostEqual(eval_regterm_negative, 0.0)
        self.assertAlmostEqual(regterm(x), regterm._eval(x))

    def test_prox(self):
        x = np.random.rand(np.random.randint(100) + 2)
        regterm = talon.optimization.NonNegativity()
        prox_regterm_positive = regterm._prox(x)
        prox_regterm_negative = regterm._prox(-x)
        np.testing.assert_almost_equal(prox_regterm_positive,
                                       np.maximum(x, 0.0))
        np.testing.assert_almost_equal(prox_regterm_negative,
                                       np.zeros_like(prox_regterm_negative))
        self.assertEqual(len(x), len(prox_regterm_positive))


class TestStructuredSparsity(unittest.TestCase):
    def test_eval(self):
        x = np.array([0.01, 0.5, 3., 4.])
        groups = [[0, 1], [2, 3]]
        weights = np.array([1.0, .2])
        regterm = talon.optimization.StructuredSparsity(1.0, groups, weights)
        eval_regterm = regterm._eval(x)
        gt = weights[0] * np.linalg.norm(x[groups[0]], 2) + weights[
            1] * np.linalg.norm(x[groups[1]], 2)
        self.assertAlmostEqual(eval_regterm, gt)
        self.assertAlmostEqual(regterm(x), regterm._eval(x))

    def test_prox(self):
        x = np.array([0.01, 0.05, 3., -4.])
        groups = [[0, 1], [2, 3]]
        weights = np.array([1.0, 2.])

        gt = x.copy()
        gt[groups[0]] = 0.0
        xn = np.linalg.norm(gt[groups[1]])
        gt[groups[1]] -= gt[groups[1]] * weights[1] / xn

        regterm = talon.optimization.StructuredSparsity(1.0, groups, weights)
        prox_regterm = regterm._prox(x, 1.0)
        np.testing.assert_almost_equal(prox_regterm, gt)


class TestNonNegativeStructuredSparsity(unittest.TestCase):
    def test_eval(self):
        x = np.array([0.01, 0.05, 3., -4.])
        groups = [[0, 1], [2, 3]]
        weights = np.array([1.0, 2.])
        regterm = talon.optimization.NonNegativeStructuredSparsity(
            1.0, groups, weights)
        self.assertAlmostEqual(regterm(x), regterm._eval(x))

    def test_prox(self):
        x = np.array([0.01, 0.05, 3., -4.])
        groups = [[0, 1], [2, 3]]
        weights = np.array([1.0, 2.])

        gt = x.copy()
        gt[gt < 0.0] = 0.0
        gt[groups[0]] = 0

        xn = np.linalg.norm(gt[groups[1]])
        gt[groups[1]] -= gt[groups[1]] * weights[1] / xn

        regterm = talon.optimization.NonNegativeStructuredSparsity(1.0, groups,
                                                                   weights)
        prox_regterm = regterm._prox(x, 1.0)
        np.testing.assert_almost_equal(prox_regterm, gt)
        self.assertTrue(all(prox_regterm >= 0.0))


class TestSolve(unittest.TestCase):
    def test_least_squares(self):
        linear_operator = 10.0 * np.eye(np.random.randint(10) + 2)
        x = np.random.rand(linear_operator.shape[1])
        y = linear_operator @ x
        solution = talon.solve(linear_operator, y, verbose='NONE')
        np.testing.assert_allclose(solution['x'], x, 1e-5, 1e-5)
        np.testing.assert_allclose(solution['fun'], 0.0, 1e-6, 1e-6)

    def test_nnls(self):
        linear_operator = 10.0 * np.eye(np.random.randint(10) + 2)
        x = np.random.rand(linear_operator.shape[1])
        y = linear_operator @ x

        regterm = talon.regularization(non_negativity=True)
        solution = talon.solve(linear_operator, y, reg_term=regterm,
                               verbose='NONE')

        np.testing.assert_allclose(solution['x'], x, 1e-5, 1e-5)
        np.testing.assert_allclose(solution['fun'], 0.0, 1e-6, 1e-6)
        self.assertTrue(all(solution['x'] >= 0))

        # test vs scipy
        data = np.random.rand(linear_operator.shape[0])
        solution = talon.solve(linear_operator, data, reg_term=regterm,
                               verbose='NONE')

        reference, residual = scipy.optimize.nnls(linear_operator, data)

        np.testing.assert_allclose(solution['fun'], 0.5 * residual ** 2, 1e-6,
                                   1e-6)
        np.testing.assert_allclose(solution['x'], reference, 1e-5, 1e-5)

    def test_group_sparsity(self):
        linear_operator = 2.0 * np.eye(10)
        x = -2.0 * np.random.rand(linear_operator.shape[1])
        x[3:7] = 0.0
        y = linear_operator @ x

        groups = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]
        weights = np.array([1.0 / np.sqrt(len(g)) for g in groups])

        regterm = talon.regularization(non_negativity=False,
                                       regularization_parameter=1.0,
                                       groups=groups, weights=weights)

        solution = talon.solve(linear_operator, y, reg_term=regterm,
                               verbose='NONE')

        self.assertTrue(all(solution['x'][groups[1]] == 0))

    def test_non_negative_group_sparsity(self):
        linear_operator = 2.0 * np.eye(10)
        x = 2.0 * np.random.rand(linear_operator.shape[1])
        x[3:7] = 0.0
        y = linear_operator @ x

        groups = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]
        weights = np.array([1.0 / np.sqrt(len(g)) for g in groups])

        regterm = talon.regularization(non_negativity=True,
                                       regularization_parameter=1.0,
                                       groups=groups, weights=weights)

        solution = talon.solve(linear_operator, y, reg_term=regterm,
                               verbose='NONE')

        self.assertTrue(all(solution['x'][groups[0]] > 0))
        self.assertTrue(all(solution['x'][groups[1]] == 0))
        self.assertTrue(all(solution['x'][groups[2]] > 0))
        self.assertTrue(all(solution['x'] >= 0))


class TestConvertSolution(unittest.TestCase):
    def test_conversion(self):
        pub_solution = dict(sol=1, objective=[1], niter=1)

        pub_solution['crit'] = 'DTOL'
        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution)
        self.assertTrue(sp_result['status'] ==
                        talon.optimization.ExitStatus.ABSOLUTE_TOLERANCE_COST)
        self.assertTrue(sp_result['success'])

        pub_solution['crit'] = 'RTOL'
        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution)
        self.assertTrue(sp_result['status'] ==
                        talon.optimization.ExitStatus.RELATIVE_TOLERANCE_COST)
        self.assertTrue(sp_result['success'])

        pub_solution['crit'] = 'XTOL'
        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution)
        self.assertTrue(sp_result['status'] ==
                        talon.optimization.ExitStatus.ABSOLUTE_TOLERANCE_X)
        self.assertTrue(sp_result['success'])

        pub_solution['crit'] = 'MAXIT'
        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution)
        self.assertTrue(sp_result['status'] ==
                        talon.optimization.ExitStatus.MAXIMUM_NUMBER_ITERATIONS)
        self.assertTrue(not sp_result['success'])

        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution,
                                                                   lol=42,
                                                                   olo=24)
        self.assertTrue(sp_result['lol'] == 42)
        self.assertTrue(sp_result['olo'] == 24)

        pub_solution = dict(sol=1, objective=[1], niter=1)
        pub_solution['crit'] = 'something not forseen'
        sp_result = talon.optimization._pyunlocbox_to_scipy_result(pub_solution)
        self.assertTrue(sp_result['status'] ==
                        talon.optimization.ExitStatus.UNKNOWN)
