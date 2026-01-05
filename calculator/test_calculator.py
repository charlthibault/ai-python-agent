import pytest
from pkg.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_addition(calculator):
    result = calculator.evaluate("3 + 5")
    assert result == 8


def test_subtraction(calculator):
    result = calculator.evaluate("10 - 4")
    assert result == 6


def test_multiplication(calculator):
    result = calculator.evaluate("3 * 4")
    assert result == 12


def test_division(calculator):
    result = calculator.evaluate("10 / 2")
    assert result == 5


def test_nested_expression(calculator):
    result = calculator.evaluate("3 * 4 + 5")
    assert result == 17


def test_complex_expression(calculator):
    result = calculator.evaluate("2 * 3 - 8 / 2 + 5")
    assert result == 7


def test_empty_expression(calculator):
    result = calculator.evaluate("")
    assert result is None


def test_invalid_operator(calculator):
    with pytest.raises(ValueError):
        calculator.evaluate("$ 3 5")


def test_not_enough_operands(calculator):
    with pytest.raises(ValueError):
        calculator.evaluate("+ 3")
