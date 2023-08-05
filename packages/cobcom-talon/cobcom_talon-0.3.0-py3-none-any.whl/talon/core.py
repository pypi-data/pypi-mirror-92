# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg

DATATYPE = np.float64


def concatenate(operators, axis=0):
    """Concatenate a sequence of linear operator along axis 0 or 1.

    This method defines the object that acts as the concatenation of the
    linear operators contained in the list/tuple `operators` along the chosen
    `axis`. The syntax is consistent with the one of `np.concatenate`.

    Args:
        operators: list or tuple of LinearOperator objects to be
            concatenated in the same axis.
        axis: int direction in which we want to concatenate the
            LinearOperator or ConcatenatedLinearOperator objects that we
            want to concatenate. Vertical concatenation is obtained for
            `axis = 0` and horizontal concatenation is obtained for
            `axis = 1` as in np.concatenate. (Default: 0)

    Returns:
        talon.core.ConcatenatedLinearOperator: the concatenated linear
            operator.
    """
    return ConcatenatedLinearOperator(operators, axis)


def normalize_atoms(generators, indices_of_generators, weights):
    """
    Prepare the input of talon.operator to get a dictionary with normalized
    atoms.

    Given a triplet ``(generators, indices_of_generators, weights)``, this
    function returns a new triplet where the ``weights`` matrix is scaled in
    such a way that the resulting linear operator has columns with norm equal
    to 1.

    Args:
        generators : np.array where each row is a generator.
        indices_of_generators : COO sparse matrix that tells which generator is
            called where in the linear operator.
        weights : COO sparse matrix that encodes the weight applied to each
            generator indexed by indices_of_generators. It has the same
            dimension as indices_of_generators.

    Returns:
        generators : the same as the input.
        indices_of_generators : the same as the input.
        weights : COO sparse matrix where each column is scaled to get a
            normalized set of atoms.

    Raises:
        ValueError : if there are empty columns in `indices_of_generators`.
    """
    if not (len(np.unique(indices_of_generators.col)) ==
            indices_of_generators.shape[1]):
        raise ValueError(
            'There are empty columns in the `indices_of_generators` matrix.')

    norms = np.zeros(indices_of_generators.shape[1])

    # squared norm of each generator
    gg = np.square(np.linalg.norm(generators, axis=1))

    # squared weights
    ww = np.square(weights.data)

    for r, c, i, w in zip(
            indices_of_generators.row,
            indices_of_generators.col,
            indices_of_generators.data,
            ww):
        norms[c] += w * gg[i]
    norms = np.sqrt(norms)

    new_data = np.zeros(weights.data.size, dtype=DATATYPE)

    for i, (c, w) in enumerate(zip(weights.col, weights.data)):
        new_data[i] = w / norms[c] if norms[c] > 0 else 1.0

    normalized_weights = sp.coo_matrix(
        (new_data, (weights.row, weights.col)),
        shape=weights.shape
    )

    return generators, indices_of_generators, normalized_weights


class AbstractLinearOperator(ABC, sp.linalg.LinearOperator):
    """Abstract class for all linear operators

    This abstract class defines the interface that all linear operators in
    talon must implement.

    """

    @property
    @abstractmethod
    def data_mask(self):
        """Returns the mask to apply to the data to keep only the entries
        covered by the linear operator."""
        pass

    @property
    @abstractmethod
    def shape(self):
        """Returns the shape of the matrix."""
        pass

    @property
    @abstractmethod
    def todense(self):
        """Returns a dense matrix representation of the linear operator."""
        pass

    @property
    @abstractmethod
    def transpose(self):
        """Returns the transpose of the linear operator."""
        pass

    @property
    def T(self):
        """Returns the transpose of the linear operator."""
        return self.transpose

    @abstractmethod
    def __matmul__(self, x):
        """Dot product between a linear operator and a vector.

        The __matmul__ method is expected to compute the dot product between
        a linear operator and a vector. It is not required to support matrix
        matrix product.

        """
        pass

    def convert_x(self, x):
        """Converts x so that it can be used on the right of a dot product.

        This method converts x so that it has the right dimensions and type to
        be used as a right operand of a dot product with a linear operator.
        That is, it asserts that A @ x will work. Raises exceptions if the
        input cannot be converted to the correct format.

        Args:
            x: The vector to test.

        Returns:
            x: A numpy array that can be used in the dot product.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.

        """

        x = np.squeeze(np.asarray(x, dtype=DATATYPE))

        # It needs to be a vector.
        if np.ndim(x) != 1:
            raise ValueError(
                f'x must be a 1D vector, but its shape is {x.shape}')

        if not len(x) == self.shape[1]:
            raise ValueError(
                f'Dimension mismatch ({len(x)} != {self.shape[1]})')

        return x

    @property
    def dtype(self):
        """Returns the data type of the linear operator"""
        return DATATYPE

    def __repr__(self):
        return f'{self.__class__.__name__}(shape={self.shape})'

    def _adjoint(self):
        """Conjugate transpose for scipy compatibility"""

        # Because we only deal with real matrices, just return the transpose.
        return self.transpose

    def _matvec(self, v):
        """Matrix vector product for scipy compatibility"""
        return self @ v


class LinearOperator(AbstractLinearOperator):
    def __init__(self, generators, indices_of_generators, weights):
        """Linear operator that maps tractography to signal space.
        The linear operator can be used to compute products with a vector.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.
        Raises:
            TypeError: If `generators` is not a numpy ndarray of float.
            TypeError: If `indices_of_generators` is not a COO scipy matrix.
            TypeError: If `weights` is not a COO scipy matrix of float64.
            ValueError: If `weights` does not have the same dimension
                as indices_of_generators.
        """
        if not isinstance(generators, np.ndarray):
            raise TypeError('Expected type for "generators" is np.ndarray.')
        if not generators.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "generators" is {}.'.format(str(DATATYPE)))

        self._generators = generators

        if not sp.isspmatrix_coo(indices_of_generators):
            raise (TypeError(
                'Expected type for "indices_of_generators" is '
                'scipy.sparse.coo_matrix.'))

        self._indices_of_generators = indices_of_generators.astype(int)

        if not sp.isspmatrix_coo(weights):
            raise (TypeError('Expected type for "weights" is np.ndarray.'))
        if not weights.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "weights" is {}.'.format(str(DATATYPE)))
        if not weights.shape == indices_of_generators.shape:
            raise ValueError(
                '"indices_of_generators" and "weights" must have the same'
                ' dimension')

        self._weights = weights

        mask = np.zeros((self._indices_of_generators.shape[0],), dtype=bool)
        mask[np.unique(self.rows)] = True
        self._data_mask = np.kron(mask,
                                  np.ones(self.generator_length, dtype=bool))

    @property
    def data_mask(self):
        """Returns the mask to apply to the data to keep only the entries
        covered by the linear operator."""
        return self._data_mask

    @property
    def columns(self):
        """int: Returns the indices of the nonzero columns."""
        return self._indices_of_generators.col

    @property
    def nb_generators(self):
        """int: Number of generators."""
        return self._generators.shape[0]

    @property
    def generator_length(self):
        """int: length of each generator (constant across generators)."""
        return self._generators.shape[1]

    @property
    def generators(self):
        """np.ndarray: Returns the generators of the linear operator."""
        return self._generators

    @property
    def indices(self):
        """np.ndarray: Returns the generator indices."""
        return self._indices_of_generators.data

    @property
    def nb_data(self):
        """int: Number of data points."""
        return self._indices_of_generators.shape[0]

    @property
    def nb_atoms(self):
        """int: Number of atoms (columns) in the linear operator."""
        return self._indices_of_generators.shape[1]

    @property
    def rows(self):
        """int: Returns the indices of the nonzero rows."""
        return self._indices_of_generators.row

    @property
    def shape(self):
        """:tuple of int: Shape of the linear operator.

        The shape is given by the number of rows and columns of the linear
        operator. The number of rows is equal to the number of data points
        times the length of the generators. The number of columns is equal to
        the number of atoms.
        """
        return self.nb_data * self.generator_length, self.nb_atoms

    @property
    def transpose(self):
        """_TransposedLinearOperator: the transpose of the linear operator."""
        return _TransposedLinearOperator(self)

    @property
    def weights(self):
        """np.ndarray: The weights of the nonzero elements"""
        return self._weights.data

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the linear operator.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.
        """

        x = self.convert_x(x)

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, column, weighted_generator in self:
            tmp = weighted_generator * x[column]
            product[self.generator_length * row:
                    self.generator_length * (row + 1)] += tmp
        return product

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        dense = np.zeros(self.shape, dtype=DATATYPE)
        length = self.generator_length
        for row, column, generator in self:
            dense[length * row: length * (row + 1), column] = generator

        return dense

    def __iter__(self):
        indices = self._indices_of_generators
        rows, cols, data = indices.row, indices.col, indices.data
        weights = self._weights.data
        for r, c, idx, w in zip(rows, cols, data, weights):
            yield r, c, self._generators[idx, :] * w


class _TransposedLinearOperator(AbstractLinearOperator):

    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        self._linear_operator = linear_operator
        self._data_mask = np.ones(self.shape[0], dtype=bool)

    @property
    def data_mask(self):
        """Returns the mask to apply to the data to keep only the entries
        covered by the linear operator."""
        return self._data_mask

    @property
    def shape(self):
        return self._linear_operator.shape[::-1]

    def __matmul__(self, y):
        """Matrix vector product (A.T @ y)

        Args:
            y: The right operand of the product. It's length must match the
                number of columns of the transposed linear operator.

        Raises:
            TypeError if y is not a numpy array.
            ValueError if the length of y does not match the number of
                columns of the transposed linear operator.
        """

        y = self.convert_x(y)

        genlen = self._linear_operator.generator_length
        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, col, weighted_generator in self._linear_operator:
            indices_range = range(genlen * row, genlen * (row + 1))
            product[col] += weighted_generator.dot(y[indices_range])
        return product

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        return self._linear_operator.todense().T

    @property
    def transpose(self):
        """LinearOperator: transpose of the transposed linear operator."""
        return self._linear_operator


class ConcatenatedLinearOperator(AbstractLinearOperator):
    def __init__(self, operators, axis):
        """Concatenated LinearOperator object

        The ConcatenatedLinearOperator class implements the vertical or
        horizontal concatenation of LinearOperator objects.

        Args:
            operators: list or tuple of LinearOperator objects to be
                concatenated in the same axis.
            axis: int direction in which we want to concatenate the
                LinearOperator or ConcatenatedLinearOperator objects that we
                want to concatenate. Vertical concatenation is obtained for
                `axis = 0` and horizontal concatenation is obtained for
                `axis = 1` as in np.concatenate. (Default: 0)

        Raises:
            TypeError: If any element of `operator` is not an instance of
                LinearOperator or ConcatenatedLinearOperator.
            TypeError: If `operators` is not a list or a tuple.
            ValueError: If `axis` is not 0 or 1.
            ValueError: If `operators` is an empty list or tuple.
            ValueError: If the operators do not have compatible dimensions.
        """
        if not type(operators) in [list, tuple]:
            raise TypeError('Expected type for `operators` is list or tuple.')

        if axis not in [0, 1]:
            raise ValueError('Expected value for `axis` is 0 or 1.')

        if len(operators) < 1:
            raise ValueError('List of operators must be non-empty.')

        if not all([isinstance(o, AbstractLinearOperator) for o in operators]):
            raise TypeError("""All concatenated operators must be linear 
            operators.""")

        if len(np.unique([op.shape[int(not axis)] for op in operators])) != 1:
            raise ValueError('Trying to concatenate linear operators with '
                             'non compatible dimensions.')

        self._axis = axis
        self._operators = operators
        self._slices = []
        self._transposed_operators = [op.T for op in self._operators]

        start_index = 0
        for linear_operator in self._operators:
            stop_index = start_index + linear_operator.shape[self._axis]
            self._slices.append(slice(start_index, stop_index))
            start_index = stop_index

        if self.axis == 0:
            masks = [op.data_mask for op in self.operators]
            self._data_mask = np.concatenate(masks, axis=0)
        else:
            self._data_mask = np.zeros_like(self.operators[0].data_mask,
                                            dtype=bool)
            for op in self.operators:
                self._data_mask += op.data_mask.astype(bool)

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the concatenated linear operator.

        Raises:
            TypeError if x is not a numpy array.
            ValueError if the length of x does not match the number of
                columns of the concatenated linear operator.
        """

        x = self.convert_x(x)

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        if self._axis == 0:
            for indices, linear_operator in zip(self._slices, self.operators):
                product[indices] = linear_operator @ x
        else:
            for indices, linear_operator in zip(self._slices, self.operators):
                product += linear_operator @ x[indices]
        return product

    @property
    def axis(self):
        """int: axis in which the concatenation was performed."""
        return self._axis

    @property
    def operators(self):
        """list: list of concatenated operators."""
        return self._operators

    @property
    def shape(self):
        """:tuple of int: Shape of the concatenated linear operator.
        """
        n_rows = np.sum([block.shape[self.axis] for block in self._operators])
        n_columns = self._operators[0].shape[int(not self.axis)]
        the_shape = n_rows, n_columns
        if self.axis:
            the_shape = the_shape[::-1]
        return the_shape

    @property
    def transpose(self):
        """TransposedConcatenatedLinearOperator: transpose of the linear
        operator."""
        return _TransposedConcatenatedLinearOperator(
            self, self._transposed_operators)

    @property
    def data_mask(self):
        """Returns the mask to apply to the data to keep only the entries
        covered by the linear operator."""
        return self._data_mask

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        all_dense = []
        for op in self.operators:
            all_dense.append(op.todense())
        return np.concatenate(all_dense, self.axis)


class _TransposedConcatenatedLinearOperator(ConcatenatedLinearOperator):
    def __init__(self, concatenated_operator, transposed_operators):
        """Transposed of a ConcatenatedLinearOperator object.

        Args:
            concatenated_operator: the ConcatenatedLinearOperator object
                of which the transpose is wanted.
        """
        self._concatenated_linear_operator = concatenated_operator

        axis = int(not self._concatenated_linear_operator.axis)

        super().__init__(transposed_operators, axis)

    @property
    def transpose(self):
        """LinearOperator: transpose of the transposed linear operator."""
        return self._concatenated_linear_operator
