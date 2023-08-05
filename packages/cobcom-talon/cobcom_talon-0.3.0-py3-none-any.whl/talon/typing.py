# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Tuple

import numpy as np
from scipy.sparse import coo_matrix

# The types used to contain the data of linear operators.
Generators = np.ndarray
Indices = coo_matrix
Weights = coo_matrix
GeneratorsIndicesWeights = Tuple[Generators, Indices, Weights]

# A single streamline must have a shape of (N, 3), but numpy does not yet
# support dtype, dimension, and size annotations.
Streamlines = Iterable[np.ndarray]
