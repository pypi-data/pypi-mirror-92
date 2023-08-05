from typing import Tuple

import numpy as np
from scipy import interpolate
from scipy.sparse import coo_matrix

import talon


def streamline_interpolation(streamline, step=0.1, spline_degree=1,
                             spline_smoothing=0.0):
    """Spline interpolation of streamlines.
    Args:
        streamline : Nx3 np.array representing a streamline.
        step : double distance between two streamlines points (default 0.1)
        spline_degree : integer must be between 1 and 5 (default 1)
        spline_smoothing: double parameter controlling the smoothness of
        the spline (default 0.0)

    Returns:
        Nx3 np.array representing the interpolated streamline

    Raises:
        ValueError: If spline_degree is not in [1,5]
        ValueError: If tnumber of points of the streamline is lower than the
                    spline order
    """
    if spline_degree < 1 or spline_degree > 5:
        raise ValueError(
            '"spline_degree" must be an integer between 1 and 5')
    if spline_degree > streamline.shape[0]:
        raise ValueError(
            '"spline_degree" must be lower than the number of points of \
            the streamline')

    s_length = np.sum(np.sqrt(np.sum(np.diff(streamline, axis=0) ** 2, 1)))

    u = np.linspace(0, 1, streamline.shape[0])
    tck, u = interpolate.splprep(
        streamline.T, u=u, k=spline_degree, s=spline_smoothing)

    streamline_points = np.int32(np.round(s_length / step))
    u_fine = np.linspace(0, 1, streamline_points)
    interpolated_points = interpolate.splev(u_fine, tck)

    return np.vstack(interpolated_points).T


def _voxelize_streamline(streamline, step=0.04):
    """Streamline to voxels.
    Args:
        streamline : Nx3 np.array representing a streamline.
        step :double minimum distance between two streamlines points

    Returns:
        out_voxel : Nx3 np.array representing the voxels in which the
        streamline passes through
        out_vector : Nx3 np.array representing direction vector of the
        streamline in each of the voxels
    """

    streamline_fine = streamline_interpolation(streamline, step)
    voxels = np.int32(np.round(streamline_fine))

    # Find where the voxel transitions occur. This is the last point in a
    # voxel.
    transitions = np.any(voxels[1:, :] != voxels[:-1, :], axis=1)
    transitions = np.nonzero(transitions)[0]
    start_points = np.hstack(([0], transitions + 1))
    end_points = np.hstack((transitions, [len(voxels) - 1]))

    # Remove single points and duplicate voxels that occur if streamlines
    # loop.
    keep = end_points != start_points
    start_points = start_points[keep]
    end_points = end_points[keep]
    _, unique_indices = np.unique(start_points, return_index=True)
    start_points = start_points[unique_indices]
    end_points = end_points[unique_indices]

    out_voxel = voxels[start_points]
    out_vector = streamline_fine[end_points] - streamline_fine[start_points]

    return out_voxel, out_vector


def voxelize_tractogram(streamlines, vertices, image_shape, step=0.04):
    """Transform a tractogram into the matrices that are necessary to build a
    linear operator.

    Args:
        streamlines : list of streamlines in voxel space. The coordinates of
            each voxel are assumed to point at the center of the voxel itself.
        vertices : Nx3 np.array, vertices of an unit sphere in which we sample
            the streamlines direction.
        image_shape : tuple, final shape of the mask image.
        step : double, streamlines interpolation step.

    Returns:
        tuple of length 2 containing

        * index_sparse : (voxel x streamlines) scipy.sparse matrix containing
            for each voxel and fiber the index of the vertices that it is
            closest to the streamline direction in that voxel.
        * length_sparse : (voxel x streamlines) scipy.sparse matrix containing
            for each voxel and fiber the length of the streamline in that voxel.

    Raises:
        ValueError: If the streamlines are not in voxel space.
    """

    s_max = np.max([np.max(s, 0) for s in streamlines], 0)
    s_min = np.min([np.min(s, 0) for s in streamlines], 0)

    if np.any(s_min < -0.5) or np.any(s_max > (np.array(image_shape) - 0.5)):
        raise ValueError(
            '"streamlines" are not in voxel space')

    locations = ([], [])
    indices = []
    lengths = []

    for i, s in enumerate(streamlines):
        # Find the voxels that the streamline crosses.
        voxels, directions = _voxelize_streamline(s, step=step)
        nonzero_voxels = np.ravel_multi_index(voxels.T, image_shape)

        # Compute the length of the streamline in a voxel.
        norms = np.linalg.norm(directions, axis=1)
        lengths.extend(norms)

        # Find the vertices that are closest to the true direction.
        directions = directions / norms[:, None]
        indices.extend(np.argmax(np.abs(np.dot(directions, vertices.T)), 1))

        # Save the location of the voxels.
        locations[0].extend(nonzero_voxels)
        locations[1].extend(np.full(len(nonzero_voxels), i))

    shape = (np.prod(image_shape), len(streamlines))
    indices = coo_matrix((indices, locations), shape, np.int64)
    lengths = coo_matrix((lengths, locations), shape, talon.core.DATATYPE)

    return indices, lengths


def diagonalize(mask):
    """Returns the matrices used to create a linear operator from a mask

    This functions transforms a volume mask into the weights and indices
    components that are necessary to build a linear operator. It is assumed
    that the all the voxels in the mask will share a common generator. The
    indexed generator is therefore unique, corresponds to index zero, and is
    weighted by the value contained in the mask at the specific voxel.

    Args:
        mask : np.ndarray with three dimensions that contains the weight to be
            associated to each voxel. Only voxels with non-zero weight are
            considered.

    Returns:
        tuple of length 2 containing

        * index_sparse : diagonal scipy.sparse matrix with a shape of (n, m)
            where n is the number of voxels of the volume and m in the number
            of voxels of the mask.
        * weight_sparse : diagonal scipy.sparse matrix with a shape of (n, m)
            containing the value of the mask at each non-zero voxel in the same
            fashion as ``index_sparse``.

    Raises:
        TypeError: If the the mask is not a numpy.ndarray.
        ValueError: If the mask does not have three dimensions.

    """

    if not isinstance(mask, np.ndarray):
        raise TypeError('The mask must be a numpy.ndarray .')

    if not (mask.ndim == 3):
        raise ValueError('The mask must be a ndarray with three dimensions.')

    flat_indices = np.flatnonzero(mask)
    weights = mask.ravel()[flat_indices]
    indices = np.zeros_like(weights)

    columns = np.arange(len(flat_indices))
    locations = (flat_indices, columns)
    shape = (mask.size, len(flat_indices))

    indices = coo_matrix((indices, locations), shape, np.int64)
    weights = coo_matrix((weights, locations), shape, talon.core.DATATYPE)
    return indices, weights


def peaks2iw(peaks: np.ndarray, vertices: np.ndarray) -> Tuple[coo_matrix,
                                                               coo_matrix]:
    """Transform a peaks volume into the indices and weights matrices that are
    necessary to build a linear operator.

    Args:
        peaks : 4D np.array, the volume containing the peaks that will be
            transformed into indices and weights
        vertices : Nx3 np.array, vertices of an unit sphere in which we sample
            the peaks direction.

    Returns:
        indices : (voxel x peaks) scipy.sparse matrix containing
            for each peak the index of the vertex that it is closest to the
            streamline direction in that voxel.
        weights : (voxel x peaks) scipy.sparse matrix with the same sparsity
            pattern as indices with value 1 in the non-zero entries.

    Raises:
        TypeError: If the peaks are not a numpy array.
        TypeError: If the vertices are not a numpy array.
        ValueError: If the peaks are not a 4D array.
        ValueError: If the size of the fourth dimension of the peaks is not a
            multiple of 3.
        ValueError: If the vertices are not a 2D array.
        ValueError: If the vertices are not a Nx3 numpy array.
    """
    if not isinstance(peaks, np.ndarray):
        raise TypeError('Peaks must be provided as a numpy array.')
    elif peaks.ndim != 4:
        raise ValueError('Peaks must be provided as a 4d numpy array.')
    elif peaks.shape[3] % 3 != 0:
        raise ValueError('The fourth dimension of the provided volume must ' +
                         'be a multiple of 3.')

    if not isinstance(vertices, np.ndarray):
        raise TypeError('Vertices must be provided as a numpy array.')
    elif vertices.ndim != 2:
        raise ValueError('Vertices must be provided as a 2d numpy array.')
    elif vertices.shape[1] != 3:
        raise ValueError('Vertices must be provided as a Nx3 numpy array.')

    n_voxels = int(np.prod(peaks.shape[: -1]))
    n_peaks_max = peaks.shape[3] // 3

    unraveled_idx = np.unravel_index(list(range(n_voxels)), peaks.shape[: -1])
    unraveled_idx = np.array(list(zip(*unraveled_idx)))

    locations = ([], [])
    indices = []
    column = 0
    for k in range(n_peaks_max):
        the_slice = slice(3 * k, 3 * (k + 1))
        for i, (x, y, z) in enumerate(unraveled_idx):
            if np.allclose(peaks[x, y, z, the_slice], (0, 0, 0)):
                continue
            locations[0].append(i)  # peak is in voxel/row i
            locations[1].append(column)
            indices.append(
                np.argmax(np.abs(peaks[x, y, z, the_slice] @ vertices.T))
            )
            column += 1

    shape = (n_voxels, column)
    indices = coo_matrix((indices, locations), shape, np.int64)
    weights = coo_matrix((np.ones(len(locations[0])), locations), shape,
                         talon.core.DATATYPE)

    return indices, weights
