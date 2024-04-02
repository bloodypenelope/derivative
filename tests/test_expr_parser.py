"""Test module for functions.expr_parser"""
import pytest
from functions import expr_parser


def test_empty():
    """Test for empty expressions"""
    assert "".join(expr_parser.Parser("").rpn) == ""


def test_strip_whitespaces():
    """Test for whitespaces in expressions"""
    assert "".join(expr_parser.Parser("x +                 y").rpn) == "xy+"
    assert "".join(expr_parser.Parser("x\t\t\t\t\n/\t\t\n\ny\n").rpn) == "xy/"


def test_bin_op():
    """Test for binary operators in expressions"""
    assert "".join(expr_parser.Parser("x + y").rpn) == "xy+"
    assert "".join(expr_parser.Parser("xy").rpn) == "xy*"
    assert "".join(expr_parser.Parser("x-y").rpn) == "xy-"
    assert "".join(expr_parser.Parser("x/y").rpn) == "xy/"
    assert "".join(expr_parser.Parser("x^y").rpn) == "xy^"
    assert "".join(expr_parser.Parser("x+y+z").rpn) == "xy+z+"


def test_prefix_op():
    """Test for prefix operators in expressions"""
    assert "".join(expr_parser.Parser("-x+y").rpn) == "xunary-y+"
    assert "".join(expr_parser.Parser("sqrtx").rpn) == "xsqrt"
    assert "".join(expr_parser.Parser("expx").rpn) == "xexp"
    assert "".join(expr_parser.Parser("lnx").rpn) == "xln"
    assert "".join(expr_parser.Parser("sinx").rpn) == "xsin"
    assert "".join(expr_parser.Parser("cosx").rpn) == "xcos"
    assert "".join(expr_parser.Parser("tgx").rpn) == "xtg"


def test_postfix_op():  # pragma: no cover
    """Test for postfix operators in expressions"""


def test_complex_expr():
    """Test for complex expressions"""
    assert "".join(expr_parser.Parser("x/(y+z)").rpn) == "xyz+/"
    assert "".join(expr_parser.Parser("sin(x^2-2lnx)").rpn) == "x2^2xln*-sin"
    assert "".join(expr_parser.Parser("exp(lnx)").rpn) == "xlnexp"
    assert "".join(expr_parser.Parser("sqrt(x^2/sinx)").rpn) == "x2^xsin/sqrt"
    assert "".join(expr_parser.Parser("x^2-3/x+20sinx").rpn) \
        == "x2^3x/-20xsin*+"
    assert "".join(expr_parser.Parser("x^x^x").rpn) == "xxx^^"


def test_skipped_muls():
    """Test for skipped multiplications in expressions"""
    assert "".join(expr_parser.Parser("xyz").rpn) == "xy*z*"
    assert "".join(expr_parser.Parser("(a+b)(c+d)").rpn) == "ab+cd+*"
    assert "".join(expr_parser.Parser("(a+b)sinx").rpn) == "ab+xsin*"
    assert "".join(expr_parser.Parser("2,3x").rpn) == "2.3x*"
    assert "".join(expr_parser.Parser("lnxexpx").rpn) == "xlnxexp*"
    assert "".join(expr_parser.Parser("(a(b(c+d)))").rpn) == "abcd+**"


def test_parenthesis():
    """Test for parenthesis in expressions"""
    assert "".join(expr_parser.Parser("(x+y)z").rpn) == "xy+z*"
    assert "".join(expr_parser.Parser("(x-y+z)sinx").rpn) == "xy-z+xsin*"
    assert "".join(expr_parser.Parser("ab/(-c)").rpn) == "ab*cunary-/"
    assert "".join(expr_parser.Parser("(a^b)^c").rpn) == "ab^c^"
    assert "".join(expr_parser.Parser("a/(b/c)").rpn) == "abc//"


def test_errors():
    """Test for errors in expressions"""
    with pytest.raises(expr_parser.ParenthesisMismatchError) as excinfo:
        _ = expr_parser.Parser("(x + 1) + 0))").rpn
        assert str(excinfo.value) == "\n(x+1)+0))\n       ^"

    with pytest.raises(expr_parser.ParenthesisMismatchError) as excinfo:
        _ = expr_parser.Parser("((x+y)").rpn
        assert str(excinfo.value) == "\n((x+y)\n^"

    with pytest.raises(expr_parser.InvalidCharacterError) as excinfo:
        _ = expr_parser.Parser("(x + 1) + x!").rpn
        assert str(excinfo.value) == "\n(x+1)+x!\n       ^"

    with pytest.raises(expr_parser.InvalidCharacterError) as excinfo:
        _ = expr_parser.Parser("abй").rpn
        assert str(excinfo.value) == "\nabй\n  ^"

    with pytest.raises(expr_parser.EntitiesPlacementError) as excinfo:
        _ = expr_parser.Parser("(a+b())").rpn
        assert str(excinfo.value) == "\n(a+b())\n     ^"

    with pytest.raises(expr_parser.EntitiesPlacementError) as excinfo:
        _ = expr_parser.Parser("1+x++3").rpn
        assert str(excinfo.value) == "\n1+x++3\n    ^"

    with pytest.raises(expr_parser.EntitiesPlacementError) as excinfo:
        _ = expr_parser.Parser("2sin").rpn
        assert str(excinfo.value) == "\n2sin\n ^^^"

    with pytest.raises(expr_parser.EntitiesPlacementError) as excinfo:
        _ = expr_parser.Parser("+2sinx").rpn
        assert str(excinfo.value) == "\n+2sinx\n^"

    with pytest.raises(expr_parser.EntitiesPlacementError) as excinfo:
        _ = expr_parser.Parser("2sinx+").rpn
        assert str(excinfo.value) == "\n2sinx+\n     ^"

    with pytest.raises(expr_parser.InvalidNumberError) as excinfo:
        _ = expr_parser.Parser("2+.").rpn
        assert str(excinfo.value) == "\n2+.\n  ^"

    with pytest.raises(expr_parser.InvalidNumberError) as excinfo:
        _ = expr_parser.Parser("1.341.2x").rpn
        assert str(excinfo.value) == "\n1.341.2x\n^^^^^^^"
