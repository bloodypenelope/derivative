from functions import expr_parser


def test_empty():
    t = expr_parser.Parser("")
    assert t.rpn == []


def test_skipped_muls():
    t = expr_parser.Parser("xyz")
    assert t.rpn == ['x', 'y', '*', 'z', '*']
