from collections import namedtuple
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Type

import numpy as np
import pyopencl as cl

import talon.core
from talon.core import AbstractLinearOperator
from talon.core import DATATYPE


# The size of the device data type.
TYPE_SIZE = 4

# Create the global OpenCL context.
_context = cl.create_some_context(interactive=False)
_queue = cl.CommandQueue(_context)

# Get the number of compute units for the selected device.
_device = _context.devices[0]
_nb_units = _device.max_compute_units

# The OpenCL program used by the product.
_programs = cl.Program(_context, """
__kernel void fast_dot(__global const float *x,
                       __global const uint *x_indices,
                       __global const float *weights,
                       __global const float *generators, 
                       __global const uint *generator_indices,
                       __global const uint *row_ends,
                       __global float *b,
                       uint generator_length, 
                       uint b_offset)
{
    uint gid = get_global_id(0);
    uint group_id = (gid + b_offset) / generator_length;
    uint lid = (gid + b_offset) % generator_length;
    
    uint x_end = row_ends[group_id];
    uint x_start = 0;
    if (group_id != 0) {
        x_start = row_ends[group_id - 1];
    }
    
    float current_result = 0;
    uint generator_id;
    
    for (uint j = x_start; j < x_end; j++) {
        generator_id = generator_indices[j];
        current_result += 
            generators[lid + generator_id * generator_length] *
            x[x_indices[j]] * weights[j];
    }
    b[gid] = current_result;
}

__kernel void transpose_dot(__global const float4 *y,
                            __global const uint *y_indices,
                            __global const float4 *generators, 
                            __global const uint *generator_indices,
                            __global const float *weights,
                            __global const uint *row_starts,
                            __global float *x,
                            uint generator_length,
                            uint y_offset)
{
    uint gid = get_global_id(0);
    uint group_id = gid / 8;
    uint lid = get_local_id(0);
    
    uint start = 0;
    uint end = row_starts[group_id];
    
    // If we are not on the first row, use the previous end as a start.
    if (group_id != 0) {
        start = row_starts[group_id - 1];
    }
    
    // The number of products per local thread.
    uint nb_products = generator_length / 4 / 8 + 1;
    
    float current_result = 0;
    local float current_gen_result[8];
    uint generator_start;
    uint y_start;
    uint k;
    for (uint i = start; i < end; i++) {
    
        current_gen_result[lid] = 0;
        generator_start = generator_indices[i] * generator_length / 4;
        y_start = (y_indices[i] - y_offset) / 4;
        for (uint j = 0; j < nb_products; j++) {
            k = lid * nb_products + j;
            if (k < generator_length / 4) {
                current_gen_result[lid] += 
                    dot(generators[generator_start + k], y[y_start + k]);
            }
        }
        
        barrier(CLK_LOCAL_MEM_FENCE);
        
        if (lid == 0) {
            float weight = weights[i];
            for (uint m = 0; m < 8; m++) {
                current_result += current_gen_result[m] * weight;
            }
        }
    }
    
    if (lid == 0) { 
        x[group_id] = current_result;
    }
}
""").build()


def _assert_enough_memory(generators, indices, chunk_size) -> None:
    """Asserts that the device has enough memory to hold a linear operator

    Asserts that the device has enough memory to hold a linear operator and
    its transpose (some memory is shared by the two). If there is not enough
    memory an exception is raised.

    Args:
        generators: The generators of the linear operator.
        indices: The generator indices of the linear operator.
        chunk_size : The product is computed by splitting the linear
            operator into chunks. This parameter determines the approximate
            chunk size. Reducing this value reduces the amount of memory
            required on the device.

    Raises:
        MemoryError: If the memory on the device is not sufficient.

    """

    # The input and output (x and y) are shared between the linear operator
    # and its transpose.
    nb_rows, nb_columns = indices.shape
    nb_generators, gen_length = generators.shape
    x_memory = nb_rows * TYPE_SIZE
    y_chunks = _chunk_sizes(chunk_size, gen_length, nb_rows) * TYPE_SIZE
    y_memory = np.sum(y_chunks)
    y_chunk_memory = np.max(y_chunks)

    # The memory for the generators is also shared.
    gen_memory = generators.size * TYPE_SIZE

    # The indices, weights, and the [x y] indices have the same size. They are
    # kept once for the linear operator and once for the transpose.
    indices_memory = len(indices.data) * TYPE_SIZE

    # We need to keep where each row starts (cols for the transpose).
    rows_start_memory = indices.shape[0] * TYPE_SIZE
    nb_chunks = len(y_chunks)
    cols_start_memory = indices.shape[1] * nb_chunks * TYPE_SIZE

    # The total amount of memory needed.
    required_memory = (
        x_memory + y_memory + gen_memory + indices_memory * 6 +
        rows_start_memory + cols_start_memory)

    # Verify if the buffer can be created individually.
    single_object_max = _device.max_mem_alloc_size
    if x_memory > single_object_max:
        raise MemoryError(
            f'The memory required for the coefficient vector is greater '
            f'than the memory than can be allocated to a single object on '
            f'your device ({x_memory} > {single_object_max}).')

    # The memory for the y is always split. We make sure we can store each
    # chunk.
    if y_chunk_memory > single_object_max:
        raise MemoryError(
            f'The memory required for the result of the product is greater '
            f'than the memory than can be allocated to a single object on '
            f'your device ({y_memory} > {single_object_max}). This may be '
            f'fixed by reducing the chunk size.')

    if indices_memory > single_object_max:
        raise MemoryError(
            f'The memory required for the index array is greater that the '
            f'memory than can be allocated to a single object on your device '
            f'({indices_memory} > {single_object_max}).')

    # There is no need to check the rows and cols start because they are always
    # smaller or equal to indices_memory.

    # Verify the global memory.
    if required_memory > _device.global_mem_size:
        raise MemoryError(
            f'Your device does not have enough memory to store the matrix and'
            f'its transpose ({required_memory} > {_device.global_mem_size}).')


def _chunk_sizes(
        desired_chunk_size: int,
        gen_length: int,
        nb_rows: int) -> np.ndarray:
    """Generate chunk sizes to split linear operator

    To reduce memory consumption, the linear operators may be split into
    chunks. However, these chunks should not cut generators and should cover
    the entire operator. This function generates valid chunk sizes which
    respect these requirements an are as close as possible to the desired
    chunk size.

    Args:
        desired_chunk_size: The target chunk size in number of rows. The
            returned chunk sizes will be close to this value.
        gen_length: The length of the generators.
        nb_rows: The number of rows of the linear operator.

    """

    # Make sure the chunks to do not cut a generator.
    chunk_size = (desired_chunk_size // gen_length + 1) * gen_length

    # Determine the number of full chunks.
    nb_chunks = int(nb_rows // chunk_size)

    # Add the remainder if any.
    remainder = int(nb_rows % chunk_size)
    chunk_sizes = [chunk_size] * nb_chunks
    if remainder != 0:
        chunk_sizes += [remainder]

    return np.array(chunk_sizes, dtype=np.int)


def _read_buffer(
        data: np.ndarray,
        dtype: Type = np.uint32) -> Optional[cl.Buffer]:
    """Creates a read only buffer from a data array.

    Args:
        data: The data to store in the buffer.
        dtype: The data type of the buffer.

    Return:
        buffer: The created buffer. If the size of the data is zero, no buffer
            is created and None is returned.
    """

    flags = cl.mem_flags.READ_ONLY
    size = data.size * TYPE_SIZE

    # Buffers cannot be created with a size of 0.
    if size == 0:
        return None

    buffer = cl.Buffer(_context, flags, size=size)
    cl.enqueue_copy(_queue, buffer, data.astype(dtype))

    return buffer


class LinearOperator(talon.core.LinearOperator):
    def __init__(self, generators, indices_of_generators, weights,
                 chunk_size=100000000):
        """Linear operator implemented with OpenCL

        A linear operator that has a sparse vector structure. The product
        between this operator and a vector is implemented using OpenCL.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.
            chunk_size : The product is computed by splitting the linear
                operator into chunks. This parameter determines the approximate
                chunk size. Reducing this value reduces the amount of memory
                required on the device.

        Raises:
            TypeError: If `generators` is not a numpy array of float.
            TypeError: If `indices_of_generators` is not a COO scipy matrix.
            TypeError: If `weights` is not a COO scipy matrix of float64.
            ValueError: If `weights` does not have the same dimension
                as indices_of_generators.
            ValueError: If `weights` and `indices_of_generators` don't have the
                same sparsity pattern.
        """

        super().__init__(generators, indices_of_generators, weights)

        # This implementation requires that the generator length be a multiple
        # of 4. This allows the use of float4 in the kernel.
        if generators.shape[1] % 4 != 0:
            raise ValueError(
                f'The length of the generators ({generators.shape[1]}) must '
                f'be a multiple of 4 to use this linear operator. Consider '
                f'padding the generators and the data with zeros.')

        _assert_enough_memory(generators, indices_of_generators, chunk_size)

        nb_generators, generator_length = generators.shape
        nb_data, nb_columns = indices_of_generators.shape

        self._generator_length = generator_length
        self._indices = indices_of_generators

        # Create a buffer of the x and y vectors and for the generators. They
        # are shared between the linear operator and its transpose and are
        # thus read/write.
        flags = cl.mem_flags.READ_WRITE
        self._x_buffer = cl.Buffer(
            _context, flags, size=self.shape[1] * TYPE_SIZE)

        self._chunk_sizes = _chunk_sizes(
            chunk_size, generator_length, self.shape[0])

        self._y_buffers = [cl.Buffer(
            _context, flags, size=c * TYPE_SIZE) for c in self._chunk_sizes]

        expanded_generators = generators.ravel().astype(np.float32)
        self._generators_buffer = _read_buffer(expanded_generators, np.float32)

        # Flatten all the 2D arrays.
        sorting_indices = np.argsort(indices_of_generators.row)
        x_indices = indices_of_generators.col[sorting_indices]
        generator_indices = indices_of_generators.data[sorting_indices]
        expanded_weights = weights.data[sorting_indices]

        # Find where the rows start.
        sorted_rows = indices_of_generators.row[sorting_indices]
        bin_count = np.bincount(sorted_rows, minlength=nb_data)
        row_starts = np.cumsum(bin_count).astype(np.uint32)

        # Create buffers for each data array used for the product.
        self._x_indices_buffer = _read_buffer(x_indices)
        self._generator_indices_buffer = _read_buffer(generator_indices)
        self._weights_buffer = _read_buffer(expanded_weights, np.float32)
        self._row_buffer = _read_buffer(row_starts)

        self._transpose = _TransposedLinearOperator(
            self, generators, indices_of_generators, weights,
            self._x_buffer, self._y_buffers, self._generators_buffer,
            self._chunk_sizes)

    @property
    def dtype(self):
        """Returns the data type of the linear operator"""
        return np.float32

    @property
    def transpose(self) -> '_TransposedLinearOperator':
        """TransposedFastLinearOperator: transpose of the linear operator."""
        return self._transpose

    def __matmul__(self, x: np.ndarray) -> np.ndarray:
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

        # Transfer the data to the device.
        cl.enqueue_copy(_queue, self._x_buffer, x.astype(np.float32))

        # Prepare the output
        product = np.zeros((self.shape[0],), dtype=np.float32)

        # Compute the probabilities on the device.
        start = 0
        for chunk_size, y_buffer in zip(self._chunk_sizes, self._y_buffers):

            stop = start + chunk_size

            _programs.fast_dot(
                _queue,
                (chunk_size,),
                None,
                self._x_buffer, self._x_indices_buffer,
                self._weights_buffer, self._generators_buffer,
                self._generator_indices_buffer,
                self._row_buffer, y_buffer,
                np.uint32(self._generator_length),
                np.uint32(start))

            cl.enqueue_copy(_queue, product[start:stop], y_buffer)
            start = stop

        return product

    def todense(self) -> np.ndarray:
        """Return the dense matrix associated with the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            Full matrix representing the linear operator.
        """
        dense = np.zeros(self.shape, dtype=DATATYPE)
        length = self._generator_length
        zipped = zip(
            self._indices.row, self._indices.col, self._indices.data,
            self.weights.data)
        for row, column, index, weight in zipped:
            generator = self.generators[index, :] * weight
            dense[length * row: length * (row + 1), column] = generator

        return dense


class _TransposedLinearOperator(AbstractLinearOperator):

    def __init__(self,
                 linear_operator: LinearOperator,
                 generators,
                 indices_of_generators,
                 weights,
                 x_buffer: cl.Buffer,
                 y_buffers: Iterable[cl.Buffer],
                 generators_buffer: cl.Buffer,
                 chunk_sizes: np.ndarray):

        self._linear_operator = linear_operator

        nb_rows, nb_columns = indices_of_generators.shape
        nb_generators, gen_length = generators.shape

        self._chunk_sizes = chunk_sizes
        self._shape = nb_columns, nb_rows * gen_length
        self._generator_length = gen_length

        # Reuse some buffers from the linear operator.
        self._generators_buffer = generators_buffer
        self._y_buffers = y_buffers
        self._x_buffer = x_buffer

        sorting_indices = np.argsort(indices_of_generators.col)
        generator_indices = indices_of_generators.data[sorting_indices]
        sorted_columns = indices_of_generators.col[sorting_indices]
        expanded_weights = weights.data[sorting_indices]
        y_indices = indices_of_generators.row[sorting_indices] * gen_length

        # Split the linear operator along the columns.
        fields = ('size', 'y', 'y_indices', 'generator_indices', 'weights',
                  'rows', 'start', 'stop')
        ChunkData = namedtuple('ChunkData', fields)
        self._chunk_data = []
        start = 0
        for chunk_size, y_buffer in zip(chunk_sizes, y_buffers):

            # Filter the y indices to keep only those of the current chunk. If
            # there are none, move on to the next chunk.
            stop = start + chunk_size
            keep = np.logical_and(y_indices >= start, y_indices < stop)
            if not np.any(keep):
                start = stop
                continue

            chunk_generator_indices = generator_indices[keep]
            chunk_y_indices = y_indices[keep]
            chunk_weights = expanded_weights[keep]
            kept_columns = sorted_columns[keep]
            bin_count = np.bincount(kept_columns, minlength=self.shape[0])
            chunk_row_starts = np.cumsum(bin_count).astype(np.uint32)

            generator_indices_buffer = _read_buffer(chunk_generator_indices)
            y_indices_buffer = _read_buffer(chunk_y_indices)
            weights_buffer = _read_buffer(chunk_weights, np.float32)
            row_buffer = _read_buffer(chunk_row_starts)

            data = ChunkData(
                chunk_size, y_buffer, y_indices_buffer,
                generator_indices_buffer, weights_buffer, row_buffer,
                start, stop)
            self._chunk_data.append(data)
            start = stop

        self._data_mask = np.ones(self.shape[0], dtype=bool)

    @property
    def data_mask(self):
        """Returns the mask to apply to the data to keep only the entries
        covered by the linear operator."""
        return self._data_mask

    @property
    def generator_length(self) -> int:
        """Returns the length of the generators."""
        return self._generator_length

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape

    @property
    def transpose(self) -> LinearOperator:
        """Returns the transpose of the linear operator."""
        return self._linear_operator

    def __matmul__(self, y: np.ndarray) -> np.ndarray:
        """"""

        # Reserve space of the final solution and for each y chunk.
        x = np.zeros((self.shape[0],), dtype=np.float32)
        x_chunk = np.empty((self.shape[0],), dtype=np.float32)

        # Compute the product chunk by chunk.
        for chunk in self._chunk_data:

            chunk_y = y[chunk.start:chunk.stop].astype(np.float32)
            cl.enqueue_copy(_queue, chunk.y, chunk_y)

            _programs.transpose_dot(
                _queue,
                (self._shape[0] * 8,),
                (8,),
                chunk.y,
                chunk.y_indices,
                self._generators_buffer,
                chunk.generator_indices,
                chunk.weights,
                chunk.rows,
                self._x_buffer,
                np.uint32(self.generator_length),
                np.uint32(chunk.start))

            cl.enqueue_copy(_queue, x_chunk, self._x_buffer)
            x += x_chunk

        return x

    def todense(self) -> np.ndarray:
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            Full matrix representing the linear operator.
        """
        return self._linear_operator.todense().T
