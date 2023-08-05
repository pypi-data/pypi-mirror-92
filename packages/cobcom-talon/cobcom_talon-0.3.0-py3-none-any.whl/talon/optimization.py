# -*- coding: utf-8 -*-
from abc import ABC
from enum import Enum

import numpy as np
from pyunlocbox import acceleration, functions, solvers
from scipy.optimize import OptimizeResult

import talon

# These keys are lambda functions in the original pyunlocbox.functions.func
# class that must be removed before serialization.
PYUNLOCBOX_KEYS_TO_REMOVE = ['y', 'A', 'At']


class RegularizationTerm(functions.func, ABC):
    def __init__(self, regularization_parameter: float):
        """Abstract base class for all regularization terms

        The optimization problem solved by `talon` is

            .. math:: \min_x 0.5 \|A x - y\|^2 + \Omega(x)

        where :math:`\Omega` is a regularization term. This class is the base
        for all concrete implementations of this term.

        Args:
            regularization_parameter: float
                The scaling factor of the regularization term. Must be a float
                greater or equal to zero.

        Raises:
            TypeError: If the regularization parameter is not a float and
                cannot be converted to a float.
            ValueError: If the regularization parameter is negative.

        """
        super().__init__()

        # Verify that the regularization parameter is a non-negative float.
        try:
            regularization_parameter = float(regularization_parameter)
        except (TypeError, ValueError):
            raise TypeError(
                f'The regularization parameter must be a float, not a '
                f'{type(regularization_parameter)}.')

        if regularization_parameter < 0:
            raise ValueError(
                f'The regularization parameter must be non-negative '
                f'({regularization_parameter} < 0).')

        self._regularization_parameter = regularization_parameter
        self._groups = None
        self._non_negativity = False
        self._weights = None

    def __call__(self, x: np.ndarray) -> float:
        """
        Call the function that defines the regularization term.
        Args:
            x: np.ndarray
                The vector on which the function must be evaluated.

        Returns:

        """
        return self._eval(x)

    def __getstate__(self):
        clean_dict = self.__dict__.copy()
        for k in PYUNLOCBOX_KEYS_TO_REMOVE:
            clean_dict.pop(k, None)
        return clean_dict

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    @property
    def groups(self) -> list:
        """
        Get the group structure associated to the regularization term.

        Returns: list
            List of lists of streamline indices.
        """
        return self._groups

    @property
    def non_negativity(self) -> bool:
        """
        Get the activation of the non-negativity constraint.

        Returns: bool
            True if the non-negativity constraint is employed, False otherwise.
        """
        return self._non_negativity

    @property
    def regularization_parameter(self) -> float:
        """
        Get the regularization parameter.

        Returns: float
            The value of the regularization parameter.
        """
        return self._regularization_parameter

    @property
    def weights(self) -> np.ndarray:
        """
        Get the weight associated to each group.

        Returns: np.ndarray
            1-dimensional numpy array with one weight per group.
        """
        return self._weights


class NoRegularization(RegularizationTerm):
    def __init__(self):
        """
        Instantiates the zero-valued regularization term.

        .. math:: \Omega(x) = 0

        """
        super().__init__(0.0)

    def _eval(self, x: np.ndarray):
        return 0.0

    def _grad(self, x: np.ndarray):
        raise NotImplementedError(
            'The gradient is not available for this regularization term.')

    def _prox(self, x: np.ndarray, _=None):
        return x


class NonNegativity(NoRegularization):
    def __init__(self):
        """
        Instantiates the non-negativity constraint regularization function.

        .. math:: \Omega(x) = \iota_{\ge 0}(x)

        """
        super().__init__()
        self._non_negativity = True

    def _grad(self, x: np.ndarray):
        raise NotImplementedError(
            'The gradient is not available for this regularization term.')

    def _prox(self, x: np.ndarray, _=None):
        return np.maximum(x, 0.0)


class StructuredSparsity(RegularizationTerm):
    def __init__(self, regularization_parameter: float, groups: list,
                 weights: np.ndarray):
        """
        Instantiates the structured sparsity regularization term.

        .. math:: \Omega(x) = \lambda \cdot \sum_{g\in G}w_g\cdot \|x_g\|_2

        Args:
            regularization_parameter: float
                Value of the regularization parameter.
            groups: list
                List of lists of streamline indices.
            weights: np.ndarray
                1-dimensional numpy array with one weight per group.
        """
        super().__init__(regularization_parameter)
        self._groups = groups
        self._weights = weights

    def _eval(self, x: np.ndarray):
        costs = [w * np.sqrt(np.sum(x[g] ** 2))
                 for g, w in zip(self._groups, self._weights)]
        return self._regularization_parameter * np.sum(costs)

    def _grad(self, x: np.ndarray):
        raise NotImplementedError(
            'The gradient is not available for this regularization term.')

    def _prox(self, x: np.ndarray, mu: float):
        v = x.copy()
        for g, w in zip(self._groups, self._weights):
            xn = np.sqrt(np.dot(v[g], v[g]))
            r = mu * self.regularization_parameter * w
            if xn > r:
                v[g] -= v[g] * r / xn
            else:
                v[g] = 0.0
        return v

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'regularization_parameter={self.regularization_parameter}, ' \
               f'n_groups={len(self._groups)})'


class NonNegativeStructuredSparsity(StructuredSparsity):
    def __init__(self, regularization_parameter, groups, weights):
        """
        Instantiates the non-negative structured sparsity regularization term.

        .. math::
            \Omega(x) = \iota_{\ge 0}(x) + \
            \lambda \cdot \sum_{g\in G}w_g\cdot \|x_g\|_2


        Args:
            regularization_parameter: float
                Value of the regularization parameter.
            groups: list
                List of lists of streamline indices.
            weights: np.ndarray
                1-dimensional numpy array with one weight per group.
        """
        super().__init__(regularization_parameter, groups, weights)
        self._non_negativity = True

    def _grad(self, x: np.ndarray):
        raise NotImplementedError(
            'The gradient is not available for this regularization term.')

    def _prox(self, x: np.ndarray, mu: float):
        v = np.maximum(x, 0.0)
        return super()._prox(v, mu)

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'regularization_parameter={self.regularization_parameter}, ' \
               f'n_groups={len(self._groups)}, ' \
               f'non_negativity=True)'


def regularization(non_negativity=False, regularization_parameter=None,
                   groups=None, weights=None):
    """Get regularization term for the optimization problem.

    By default this method returns an object encoding the regularization term

        .. math:: \Omega(x) = 0 .

    If `regularization_parameter`, `groups` and `weights` are all not None it
    returns the structured sparsity regularization.

        .. math:: \Omega(x) = \lambda \sum_{g\in G} w_g \|x_g\|_2

    where :math:`\lambda` is `regularization_parameter`, :math:`w_g` is the
    entry of `w` associated to `g`, :math:`x_g` is the subset of entries
    of *x* encoded by the indices of *g* and `G` is the list of groups.

    If non_negativity is True it adds the non-negativity constraint to the
    regularization term.

        .. math:: \Omega(x) \leftarrow \Omega(x) + \iota_{\ge 0}(x) .

    Args:
        non_negativity: boolean (default = False)
        regularization_parameter: float. Must be >= 0 (default = None)
        groups: list of lists where each element encodes the indices of the
            streamlines belonging to a single group. (default = None).

            E.g.: ``groups = [[0,2,5], [1,3,4,6], [7,8,9]]``.
        weights: ndarray of the same length as `groups`. Weight associated to
            each group. (default = None)

    Returns:
        instance of one between

        * ``talon.optimize.NoRegularization``;
        * ``talon.optimize.NonNegativity``;
        * ``talon.optimize.StructuredSparsity``;
        * ``talon.optimize.NonNegativeStructuredSparsity``.

    Raises:
        ValueError: If weights and groups do not have the same length.
        ValueError: If regularization_parameter < 0 .
    """
    if regularization_parameter is None or groups is None or weights is None:
        is_structure_sparsity = False
    elif regularization_parameter == 0.0:
        is_structure_sparsity = False
    elif regularization_parameter < 0.0:
        raise ValueError('Negative regularization parameter not allowed.')
    elif len(groups) == len(weights):
        is_structure_sparsity = True
    else:
        raise ValueError('`groups` and `weights` are not coherent objects. '
                         'Check the type and the length.')

    if non_negativity:
        if is_structure_sparsity:
            return NonNegativeStructuredSparsity(regularization_parameter,
                                                 groups, weights)
        else:
            return NonNegativity()
    else:
        if is_structure_sparsity:
            return StructuredSparsity(regularization_parameter, groups,
                                      weights)
        else:
            return NoRegularization()


class ExitStatus(Enum):
    """
    Exit criteria of the optimization routine.
    """
    UNKNOWN = -1
    MAXIMUM_NUMBER_ITERATIONS = 0
    ABSOLUTE_TOLERANCE_COST = 1
    RELATIVE_TOLERANCE_COST = 2
    ABSOLUTE_TOLERANCE_X = 3


def _pyunlocbox_to_scipy_result(pub_result: dict, **kwargs):
    sp_result = OptimizeResult()

    if pub_result['crit'] == 'DTOL':
        new_status = ExitStatus.ABSOLUTE_TOLERANCE_COST
    elif pub_result['crit'] == 'RTOL':
        new_status = ExitStatus.RELATIVE_TOLERANCE_COST
    elif pub_result['crit'] == 'XTOL':
        new_status = ExitStatus.ABSOLUTE_TOLERANCE_X
    elif pub_result['crit'] == 'MAXIT':
        new_status = ExitStatus.MAXIMUM_NUMBER_ITERATIONS
    else:
        new_status = ExitStatus.UNKNOWN
    sp_result['status'] = new_status

    sp_result['success'] = sp_result['status'].value > 0
    sp_result['message'] = pub_result['crit']
    sp_result['fun'] = pub_result['objective'][-1]
    sp_result['nit'] = pub_result['niter']
    sp_result['x'] = pub_result['sol']

    for key, value in kwargs.items():
        sp_result[key] = value

    return sp_result


def solve(linear_operator: talon.core.LinearOperator, data: np.ndarray,
          reg_term: RegularizationTerm = None,
          cost_reltol: float = 1e-6, x_abstol: float = 1e-6,
          max_nit: int = 1000, x0: np.ndarray = None,
          verbose: str = 'LOW') -> OptimizeResult:
    """Fit the solution.

    This routine finds the `x` that solves the problem

        .. math:: \min_x 0.5 \|A x - y\|^2 + \Omega(x)

    where `x` is the vector of coefficients to be retrieved, `A` is the linear
    operator, `y` is the data vector and :math:`\Omega` is defined as in
    ``talon.regularization``.

    Args:
        linear_operator: linear operator endowed with the @ operation.
        data: ndarray of data to be fit. First dimension must be compatible
            with the second of `linear_operator`.
        reg_term: regularization term defined by talon.regularization.
            (default: :math:`\Omega(x) = 0.0`)
        cost_reltol: float relative tolerance on the cost (default = 1e-6).
        x_abstol: float mean abs tolerance on the variable (default = 1e-6).
        max_nit: int maximum number of iterations (default = 1000).
        x0: ndarray starting value for the optimization. The length must be the
            equal to the second dimension of `linear_operator`. (default=zeros)
        verbose : {'NONE', 'LOW', 'HIGH', 'ALL'} The log level : ``'NONE'``
            for no log, ``'LOW'`` for resume at convergence, ``'HIGH'`` for
            info at all solving steps, ``'ALL'`` for all possible outputs,
            including at each steps of the proximal operators computation
            (default='LOW').

    Return:
     scipy.optimize.OptimizeResult: dictionary with the following fields

         * x : estimated minimizer of the cost function.
         * status : attribute of talon.optimization.ExitStatus enumeration.
         * message : string that explains the reason for termination.
         * fun : evaluation of each term at the minimizer.
         * nit : number of performed iterations.
         * reg_param: value of the regularization parameter.
    """
    fit_term = functions.norm_l2(y=data, lambda_=0.5)
    fit_term.A = lambda x: linear_operator @ x
    fit_term.At = lambda x: linear_operator.T @ x

    if reg_term is None:
        reg_term = regularization()

    my_acceleration = acceleration.fista_backtracking()
    the_solver = solvers.forward_backward(accel=my_acceleration, step=0.5)

    if x0 is None:
        x0 = np.zeros(linear_operator.shape[1], dtype=talon.core.DATATYPE)

    solution = solvers.solve([fit_term, reg_term], x0, the_solver,
                             rtol=cost_reltol, xtol=x_abstol, maxit=max_nit,
                             verbosity=verbose)
    return _pyunlocbox_to_scipy_result(solution, regularization_term=reg_term)
