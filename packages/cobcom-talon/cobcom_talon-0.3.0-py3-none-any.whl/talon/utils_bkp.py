import numpy as np
from scipy.sparse import coo_matrix


def remove_empty_rows(generators, indices, weights):
    """Removes the empty rows of a GIW matrix

    Removes the empty rows of a Generator-Indices-Weights (GIW) matrix. The
    resulting matrix has the same number of columns, but fewer rows.

    Args:
        generators: The generators of the matrix.
        indices: The generator indices of the matrix.
        weights: The generator weights of the matrix.

    Returns:
        generator: The generators of the new matrix.
        new_indices: The new indices of the matrix, adjusted for the row
            removal.
        new_weights: The generator weights of the matrix.

    """

    # Build a map from the old rows to the new ones and map the old rows.
    unique_rows = np.unique(indices.row)
    mapping = {r: i for i, r in enumerate(unique_rows)}
    new_rows = [mapping[r] for r in indices.row]

    new_shape = (len(unique_rows), indices.shape[1])

    # Create the new matrix with the removed rows.
    indices_args = (indices.data, (new_rows, indices.col))
    new_indices = coo_matrix(indices_args, shape=new_shape)
    weights_args = (weights.data, (new_rows, weights.col))
    new_weights = coo_matrix(weights_args, shape=new_shape)

    return generators, new_indices, new_weights
