import numpy as _np

import talon.core as _core


class LinearOperator(_core.LinearOperator):

    def __init__(self, generators, indices_of_generators, weights):
        """A LinearOperator that computes products quickly.

        The FastLinearOperator class implements a linear operator optimized to
        compute matrix-vector products quickly. It is single threaded and
        written in pure Python, which makes it a good default choice for linear
        operators.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.

        Raises:
            TypeError: If generators is not a numpy ndarray of float64.
            TypeError: If indices_of_generators is not a COO scipy matrix.
            TypeError: If weights is not a COO scipy matrix of float64.
            ValueError: if weights does not have the same dimension
                as indices_of_generators.
            ValueError: if weights and indices_of_generators don't have the
                same sparsity pattern.

        """

        super().__init__(generators, indices_of_generators, weights)

        # Find the indices of the row which are not empty. This allows the
        # linear performance to be independent of the number of empty rows.
        row_indices = _np.unique(self.rows)

        # The product is computed row by row. Here, we precompute which
        # generators are multiplied by which weight and x, and where the
        # result is placed.
        row_elements = [[] for _ in range(self.nb_data)]
        for i, r in enumerate(self.rows):
            row_elements[r].append(i)
        row_elements = [_np.array(re) for re in row_elements if len(re) != 0]

        # The indices of the generator, for each row.
        row_generators = [self.indices[r] for r in row_elements]

        # The indices of nonzero columns for each row.
        row_columns = [self.columns[r] for r in row_elements]

        # The weights of the nonzero elements for each row.
        row_weights = [self.weights[r] for r in row_elements]

        length = self.generator_length

        def row_slice(row):
            return slice(length * row, length * (row + 1))

        row_slices = [row_slice(r) for r in row_indices]

        self._row = list(zip(row_columns, row_generators, row_weights,
                             row_slices))

    @property
    def transpose(self):
        """Returns the transpose of the linear operator."""
        return _TransposedFastLinearOperator(self)

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

        product = _np.zeros(self.shape[0], dtype=_core.DATATYPE)

        for elements, generator_indices, weights, row_slice in self._row:
            row_x = x[elements] * weights
            row_generators = self.generators[generator_indices, :]
            product[row_slice] = _np.dot(row_generators.T, row_x)

        return product


class _TransposedFastLinearOperator(_core._TransposedLinearOperator):
    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        super().__init__(linear_operator)

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

        product = _np.zeros(self.shape[0], dtype=_core.DATATYPE)
        for (elements, generator_indices,
             weights, row_slice) in self._linear_operator._row:
            row_y = y[row_slice]
            row_generators = self._linear_operator.generators[
                             generator_indices, :]
            product[elements] += row_generators.dot(row_y) * weights

        return product