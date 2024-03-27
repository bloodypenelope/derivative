"""Test module for functions.expr_parser"""
import pytest
from functions import expr_parser


@pytest.mark.parametrize("expression, expected_rpn",
                         [("", "")])
def test_empty(expression, expected_rpn):
    """Test for empty expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn",
                         [("x +                 y", "xy+"),
                          ("x\t\t\t\t\n/\t\t\n\ny\n", "xy/")])
def test_strip_whitespaces(expression, expected_rpn):
    """Test for whitespaces in expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn",
                         [("x + y", "xy+"),
                          ("xy", "xy*"),
                          ("x-y", "xy-"),
                          ("x/y", "xy/"),
                          ("x^y", "xy^"),
                          ("x+y+z", "xy+z+")])
def test_bin_op(expression, expected_rpn):
    """Test for binary operators in expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn",
                         [("-x+y", "xunary-y+"),
                          ("sqrtx", "xsqrt"),
                          ("cbrtx", "xcbrt"),
                          ("expx", "xexp"),
                          ("lnx", "xln"),
                          ("sinx", "xsin"),
                          ("cosx", "xcos"),
                          ("tgx", "xtg")])
def test_prefix_op(expression, expected_rpn):
    """Test for prefix operators in expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn", [])  # pragma: no cover
def test_postfix_op(expression, expected_rpn):
    # pylint: disable=unused-argument
    """Test for postfix operators in expressions"""


@pytest.mark.parametrize("expression, expected_rpn",
                         [("x/(y+z)", "xyz+/"),
                          ("sin(x^2-2lnx)", "x2^2xln*-sin"),
                          ("exp(lnx)", "xlnexp"),
                          ("sqrt(x^2/sinx)", "x2^xsin/sqrt"),
                          ("x^2-3/x+20sinx", "x2^3x/-20xsin*+"),
                          ("x^x^x", "xxx^^")])
def test_complex_expr(expression, expected_rpn):
    """Test for complex expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn",
                         [("xyz", "xy*z*"),
                          ("(a+b)(c+d)", "ab+cd+*"),
                          ("(a+b)sinx", "ab+xsin*"),
                          ("2,3x", "2.3x*"),
                          ("lnxexpx", "xlnxexp*"),
                          ("(a(b(c+d)))", "abcd+**")])
def test_skipped_muls(expression, expected_rpn):
    """Test for skipped multiplications in expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_rpn",
                         [("(x+y)z", "xy+z*"),
                          ("(x-y+z)sinx", "xy-z+xsin*"),
                          ("ab/(-c)", "ab*cunary-/"),
                          ("(a^b)^c", "ab^c^"),
                          ("a/(b/c)", "abc//")])
def test_parenthesis(expression, expected_rpn):
    """Test for parenthesis in expressions"""
    assert "".join(expr_parser.Parser(expression).rpn) == expected_rpn


@pytest.mark.parametrize("expression, expected_error, expected_error_message",
                         [("(x + 1) + 0))", expr_parser.ParenthesisMismatchError,
                           "\n(x+1)+0))\n       ^"),
                          ("((x+y)", expr_parser.ParenthesisMismatchError,
                           "\n((x+y)\n^"),
                          ("(x + 1) + x!", expr_parser.InvalidCharacterError,
                           "\n(x+1)+x!\n       ^"),
                          ("abй", expr_parser.InvalidCharacterError,
                           "\nabй\n  ^"),
                          ("(a+b())", expr_parser.EntitiesPlacementError,
                           "\n(a+b())\n     ^"),
                          ("1+x++3", expr_parser.EntitiesPlacementError,
                           "\n1+x++3\n    ^"),
                          ("2sin", expr_parser.EntitiesPlacementError,
                           "\n2sin\n ^^^"),
                          ("+2sinx", expr_parser.EntitiesPlacementError,
                           "\n+2sinx\n^"),
                          ("2sinx+", expr_parser.EntitiesPlacementError,
                           "\n2sinx+\n     ^"),
                          ("2+.", expr_parser.InvalidNumberError,
                           "\n2+.\n  ^"),
                          ("1.341.2x", expr_parser.InvalidNumberError,
                           "\n1.341.2x\n^^^^^^^")])
def test_errors(expression, expected_error, expected_error_message):
    """Test for errors in expressions"""
    with pytest.raises(expected_error) as excinfo:
        _ = expr_parser.Parser(expression).rpn
    assert str(excinfo.value) == expected_error_message
