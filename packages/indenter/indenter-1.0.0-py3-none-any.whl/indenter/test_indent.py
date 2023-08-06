from . import Indenter


def test_indent():
    ind = Indenter()
    with ind:
        assert str(ind) == "  "


def test_usage_without_with():
    ind = Indenter()
    assert str(ind) == ""


def test_inline():
    with Indenter() as ind:
        assert str(ind) == "  "


def test_start():
    ind = Indenter(start=1)
    assert str(ind) == "  "
    with ind:
        assert str(ind) == "    "


def test_nesting():
    ind = Indenter()
    with ind:
        assert str(ind) == "  "
        with ind:
            assert str(ind) == "    "
        assert str(ind) == "  "


def test_nesting_with_start():
    ind = Indenter(start=1)
    with ind:
        assert str(ind) == "    "
        with ind:
            assert str(ind) == "      "


def test_multiple_indenters():
    inda = Indenter(symbol="*")
    indb = Indenter(symbol="$")
    with inda:
        assert str(inda) == "*"
        with indb:
            assert str(inda) == "*"
            assert str(indb) == "$"
            with indb:
                assert str(inda) == "*"
                assert str(indb) == "$$"
                with inda:
                    assert str(inda) == "**"
                    assert str(indb) == "$$"
