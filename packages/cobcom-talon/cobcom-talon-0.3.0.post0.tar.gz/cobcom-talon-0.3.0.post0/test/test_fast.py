from test.test_core import TestLinearOperator

import talon.fast


class TestFastLinearOperator(TestLinearOperator):
    """Test the talon.core.FastLinearOperator class."""

    @property
    def linear_operator(self):
        return talon.fast.LinearOperator
