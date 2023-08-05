import importlib.util

from test.test_core import TestLinearOperator

# Run the opencl tests only if pyopencl is available.
if importlib.util.find_spec('pyopencl') is not None:

    import talon.opencl

    class TestFastLinearOperator(TestLinearOperator):
        """Test the talon.core.FastLinearOperator class."""

        @property
        def linear_operator(self):
            return talon.opencl.LinearOperator
