import unittest
from pylambdalib.elements import Val, ValuesInConflictError, ValueGroup

class TestLambdaError(unittest.TestCase):

    def test_adding_equal_values_raises_error(self):
        def add_values():
            value_group = ValueGroup()
            value_group.add(Val("1671807295..1.:@variableMock|valorMock|0"))
            value_group.add(Val("1671807295..1.:@variableMock|valorMock|0"))
        self.assertRaises(
            ValuesInConflictError,
            add_values
        )

    def test_adding_conflicting_values_raises_error(self):
        def add_values():
            value_group = ValueGroup()
            value_group.add(Val("1671807295..1.:@variableMock|valorMock1|0"))
            value_group.add(Val("1671807298..1.:@variableMock|valorMock2|0"))
        self.assertRaises(
            ValuesInConflictError,
            add_values
        )

    def test_adding_non_conflicting_values(self):
        def helper_func():
            def add_values():
                value_group = ValueGroup()
                value_group.add(Val("1671807295.1671807297.1.:@variableMock|valorMock1|0"))
                value_group.add(Val("1671807298..1.:@variableMock|valorMock2|0"))

            self.assertRaises(
                ValuesInConflictError,
                add_values
            )
        self.assertRaises(
            AssertionError,
            helper_func
        )


if __name__ == "__main__":
    unittest.main()