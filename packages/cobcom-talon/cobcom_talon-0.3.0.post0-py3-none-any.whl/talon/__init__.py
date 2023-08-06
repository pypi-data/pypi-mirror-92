__version__ = '0.3.0.post0'

import importlib.util
import sys
from typing import Tuple

import numpy as np
import scipy.sparse as sp

import talon.fast
import talon.utils
from talon.core import LinearOperator
from talon.core import concatenate
from talon.core import normalize_atoms as normalize
from talon.optimization import regularization
from talon.optimization import solve
from talon.voxelization import diagonalize, peaks2iw
from talon.voxelization import voxelize_tractogram as voxelize


# Verify if OpenCL is available.
if importlib.util.find_spec('pyopencl') is not None:
    import talon.opencl


def operator(generators, indices_of_generators, weights, operator_type='fast'):
    r"""Create a LinearOperator object.

    This method defines the object that describes the linear operator by means
    of its fundamental components. These components are a set of generators, a
    table that encodes the non-zero entries of the operator and indexes the
    proper generator in each entry and another table that encodes the weight
    applied to each called generator in the linear operator.

    Each block of entries of the linear operator A is given by

        .. math:: A[k\cdot i\dots k\cdot(i+1), j] = g_{T_{i,j}} \cdot w_{i,j}

    where `k` is the length of the generators, `T` is the table of indices and
    `w` is the table of weights.

    Args:
        generators : np.array where each row is a generator.
        indices_of_generators : COO sparse matrix that tells which generator is
            called where in the linear operator.
        weights : COO sparse matrix that encodes the weight applied to each
            generator indexed by indices_of_generators. It has the same
            dimension as indices_of_generators.
        operator_type (optional): string
            Operator type to use. Accepted values are ``'fast'``, ``'opencl'``,
            and ``'reference'``. The latter is intended to be used only for
            testing purposes. (default = `fast`).

    Returns:
        talon.core.LinearOperator: the wanted linear operator.

    Raises:
        ValueError: If `reference_type` is not ``'fast'`` or ``'reference'``.
    """

    args = (generators, indices_of_generators, weights)

    if operator_type == 'fast':
        return talon.fast.LinearOperator(*args)

    elif operator_type == 'reference':
        return talon.core.LinearOperator(*args)

    elif operator_type == 'opencl':

        if 'talon.opencl' not in sys.modules:
            raise RuntimeError(
                'The OpenCL implementation of operators is not available '
                'on your system.')
        return talon.opencl.LinearOperator(*args)

    raise ValueError(
        f'Invalid reference type "{operator_type}". Should be "fast", '
        f'"opencl", or "reference".')


def zeros(shape: Tuple[int, int], dtype: type = np.float64) -> LinearOperator:
    r"""Create a zero filled linear operator

    Returns a zero filled talon linear operator. Useful in combination with
    talon.concatenate.

    Args:
        shape: The shape of the linear operator.
        dtype (optional): The datatype of the linear operator.

    Returns:
        A talon linear operator filled with zeros.

    """
    return operator(
        np.zeros((1, 1), dtype=dtype), sp.coo_matrix(shape, dtype=np.int64),
        sp.coo_matrix(shape, dtype=dtype), operator_type='fast')
