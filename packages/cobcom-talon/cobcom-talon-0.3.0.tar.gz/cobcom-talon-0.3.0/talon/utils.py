from typing import Iterable

import numpy as np
import scipy.sparse as sp

import talon


def check_pattern_iw(indices_of_generators: sp.coo_matrix,
                     weights: sp.coo_matrix) -> None:
    """
    Check if the sparsity pattern of the indices and the weights are the same.

    This function performs a complete check on the sparsity pattern of the
    `indices_of_generators` and the `weights` matrices. If the two matrices
    have a different number of non-empty entries or the non-empty entries are
    in different locations, it raises an error.

    If the two matrices came out of `talon.voxelization`, this check is not
    necessary.

    Note:
        This function is **very** expensive in terms of memory and time.


    Args:
        indices_of_generators : sp.coo_matrix of the indices.
        weights : sp.coo_matrix of the weights.
    Raises:
        ValueError: If `weights` and `indices_of_generators` don't have the
            same sparsity pattern.
    """
    if not (
            len(weights.data) == len(indices_of_generators.data) and
            np.array_equal(
                sorted(zip(weights.row, weights.col)),
                sorted(zip(indices_of_generators.row,
                           indices_of_generators.col)))):
        raise ValueError(
            '"indices_of_generators" and "weights" must have the same'
            ' sparsity pattern')


def concatenate_giw(giws: Iterable, axis: int = 0) -> tuple:
    """Concatenates generators, indices, and weights along an existing axis

    The indices and weights are concatenated along the supplied axis and the
    generators along axis 1. The generators must have the same number of
    columns. The indices and weights must have the same shape, except in
    the dimension corresponding to axis.

    Args:
        giws: An iterable of (generator, indices, weights) to concatenate
            e.g. [(g1, i1, w1), (g2, i2, w2)].
        axis: The axis along which the indices and weights will be joined.
            Default is 0.

    Returns:
        The concatenated generators, indices, and weights.

    """

    # Axis must be 0 or 1.
    if axis not in (0, 1):
        raise ValueError(f'\'axis\' must be 0 or 1, not {axis}.')

    generators, indices, weights = zip(*giws)
    nb_generators = np.zeros(len(generators))
    nb_generators[1:] = np.cumsum([g.shape[0] for g in generators])[:-1]

    # The generators must have the same number of columns.
    nb_columns = [g.shape[1] for g in generators]
    if len(set(nb_columns)) != 1:
        raise ValueError(
            f'The generators do not all have the same number of columns '
            f'({nb_columns}). They cannot be concatenated.')

    new_generators = np.vstack(generators)

    # The indices of the generators need to be offset by the sum of the number
    # generators in the previous matrices.
    offset_indices = [sp.coo_matrix((i.data + n, (i.row, i.col)), i.shape)
                      for i, n in zip(indices, nb_generators)]

    # Stack using sparse tools.
    stack = sp.hstack if axis == 0 else sp.vstack
    new_indices = stack(offset_indices, dtype=np.int64)
    new_weights = stack(weights, dtype=talon.core.DATATYPE)

    return new_generators, new_indices, new_weights


def directions(number_of_points: int = 180) -> np.ndarray:
    """
    Get a list of 3D vectors representing the directions of the fibonacci
    covering of a hemisphere of radius 1 computed with the golden spiral method.
    The :math:`z` coordinate of the points is always strictly positive.

    Args:
        number_of_points : number of points of the wanted covering (default=180)

    Returns:
        ndarray : ``number_of_points`` x 3 array with the cartesian coordinates
            of a point of the covering in each row.

    Raises:
        ValueError : if ``number_of_points <= 0`` .

    References:
        https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere/44164075#44164075
    """
    number_of_points = int(number_of_points)

    if number_of_points <= 0:
        raise ValueError('The number of points for the covering must be >= 1 .')

    n = 2 * number_of_points
    indices = np.arange(0, n, dtype=float) + 0.5

    phi = np.arccos(1 - 2 * indices / n)
    theta = np.pi * (1 + np.sqrt(5)) * indices

    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)

    x, y, z = map(lambda a: a[:number_of_points], [x, y, z])

    points = np.c_[x, y, z].astype(talon.core.DATATYPE)

    return np.asarray([p / np.linalg.norm(p) for p in points])


def mask_data(data: np.ndarray,
              linear_operator: talon.core.LinearOperator) -> np.ndarray:
    """
    Mask the data using the mask that covers only the entries that are affected
    by the linear operator. This prevents numerical errors in the solution of
    the optimization problem.

    Args:
         data : np.ndarray one dimensional array that contains the data to mask.
         linear_operator : LinearOperator object that contains the
            self.data_mask attribute to be used as a mask.
    Return:
         np.ndarray with the same dimension as data where the entries
         corresponding to the False entries of the mask have been set to zero.
    """
    data[linear_operator.data_mask == False] = 0.0
    return data
