"""Test module for functions.function"""
import pytest
from functions import function


@pytest.mark.parametrize("func, expected_str",
                         [(None, ""),
                          ("", "")])
def test_empty(func, expected_str):
    """Test for empty functions"""
    assert str(function.Function(func)) == expected_str


@pytest.mark.parametrize("rpn, expected_str", [([], "")])
def test_build_empty_tree(rpn, expected_str):
    """Test for building functions from empty rpn tokens list"""
    func = function.Function()
    func.build_tree(rpn)
    assert str(func) == expected_str


@pytest.mark.parametrize("func, expected_str",
                         [("x^2+2x+2", "x^2.0+2.0*x+2.0"),
                          ("(a+b)/c", "(a+b)/c"),
                          ("sin(x-1/y)", "sin(x-1.0/y)"),
                          ("e^(lnx/lnpi)", "e^(ln(x)/ln(pi))"),
                          ("tg(-cos(e^exp(2/2)))", "tg(-(cos(e^exp(2.0/2.0))))"),
                          ("0/0", "undefined")])
def test_build_func(func, expected_str):
    """Test for building functions"""
    assert str(function.Function(func)) == expected_str


@pytest.mark.parametrize("func, expected_str",
                         [("2x + x", "3.0*x"),
                          ("x + y + z + x", "2.0*x+y+z"),
                          ("e^lnx", "x"),
                          ("sinx^2 + cosx^2", "1.0"),
                          ("x * x^2", "x^3.0"),
                          ("x^1/2 * x^2", "x^3.0/2.0"),
                          ("0/0", "undefined")])
def test_simplify(func, expected_str):
    """Test for simplifying functions"""
    assert str(function.Function(func).simplify()) == expected_str


@pytest.mark.parametrize("func, point, expected_str",
                         [("2x + x", {'x': 2}, "6.0"),
                          ("e^x", {'x': 0}, "1.0"),
                          ("sinx^2+cosx^2", {'x': 0}, "1.0"),
                          ("x^3-lnx", {'x': 1}, "1.0"),
                          ("x^2-siny+exp(z)", {'x': 2, 'y': 0, 'z': 0}, "5.0"),
                          ("x^2*x^3", {}, "x^2.0*x^3.0")])
def test_calculate(func, expected_str, point):
    """Test for calculating functions"""
    assert str(function.Function(func).calculate(**point)) == expected_str


@pytest.mark.parametrize("func, variable, point, expected_str",
                         [("x^2-2z", 'x', {'x': 5, 'z': 2}, "10.0"),
                          ("cosx+yx", 'x', {'x': 0, 'y': 2}, "2.0"),
                          ("e^sinx", 'x', {'x': 0}, "1.0"),
                          ("lnx", 'x', {'x': 5}, "0.2"),
                          ("2x+y^3-sin(tg(z))", 'w', {'x': 10, 'y': 20, 'z': 30}, "0.0")])
def test_derive(func, variable, point, expected_str):
    """Test for differentiating functions at some point"""
    assert str(function.Function(func).derive(
        variable, **point)) == expected_str


@pytest.mark.parametrize("func, variable, expected_str",
                         [("-sin(x^3)", 'x', "-(3.0)*x^2.0*cos(x^3.0)"),
                          ("(x-1)/(x+1)", 'x', "2.0/(x+1.0)^2.0"),
                          ("sqrt(x^2)", 'x', "x/sqrt(x^2.0)"),
                          ("cbrt(x^3)", 'x', "x^2.0/(x^6.0)^(1.0/3.0)"),
                          ("exp(cos(x))", 'x', "-(exp(cos(x)))*sin(x)"),
                          ("", 'x', "")])
def test_diff(func, variable, expected_str):
    """Test for differentiating functions"""
    assert str(function.Function(func).diff(variable)) == expected_str


@pytest.mark.parametrize("func, point, expected_error",
                         [("x^y", {'x': 0, 'y': 0}, ZeroDivisionError),
                          ("x^(1/2)", {'x': -1}, ValueError),
                          ("x^(1/3)", {'x': -2}, ValueError),
                          ("sqrt(x-5)", {'x': 4}, ValueError),
                          ("ln(sin(x))", {'x': 0}, ValueError),
                          ("ln(x^2-4x+3)", {'x': 2}, ValueError)])
def test_calculate_errors(func, point, expected_error):
    """Test for errors in functions that may occur during calculation"""
    with pytest.raises(expected_error):
        _ = function.Function(func).calculate(**point)


@pytest.mark.parametrize("func, variable, point, expected_error",
                         [("ln(x+y-z^2)", 'x', {'x': 0, 'y': 0}, ValueError),
                          ("tg(x/2)", 'x', {}, ValueError),
                          ("", 'x', {'x': -2}, ValueError),
                          ("sqrt(x^2)", 'x', {'x': 0}, ValueError),
                          ("ln(sin(x))", 'x', {'x': 0}, ValueError),
                          ("e^cosx*1/tgx", 'x', {'x': 0}, ValueError)])
def test_derive_errors(func, variable, point, expected_error):
    """Test for errors in functions that may occur while taking derivative"""
    with pytest.raises(expected_error):
        _ = function.Function(func).derive(variable, **point)
