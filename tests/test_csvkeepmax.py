import io
import pytest

import sacsv.csvkeepmax as m


def test_string_value_raises_value_error(monkeypatch):
    content = "a,b\nfoo,2\nbar,4\nbaz,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(column="a")

    content = "a,b\nfoo,2\nbar,4\nbaz,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(column="a", group_by="b")


def test_each_row_with_global_max_of_int_is_printed(monkeypatch, capsys):
    content = "a,b\nfoo,2\nfoo,4\nbar,6\nbaz,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(column="b")

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "bar,6\r\n"
        "baz,6\r\n"
    )


def test_each_row_with_global_max_of_float_is_printed(monkeypatch, capsys):
    content = "a,b\nfoo,1e1\nfoo,1e2\nbar,1e3\nbaz,1e3\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(column="b")

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "bar,1e3\r\n"
        "baz,1e3\r\n"
    )


def test_each_row_with_group_max_of_int_is_printed(monkeypatch, capsys):
    content = "a,b\nfoo,2\nfoo,4\nbar,6\nbaz,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(column="b", group_by=["a"])

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "bar,6\r\n"
        "baz,6\r\n"
        "foo,4\r\n"
    )


def test_each_row_with_group_max_of_float_is_printed(monkeypatch, capsys):
    content = "a,b\nfoo,1e1\nfoo,1e2\nbar,1e3\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(column="b", group_by=["a"])

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "bar,1e3\r\n"
        "foo,1e2\r\n"
    )


def test_rows_with_missing_values_are_ignored(monkeypatch, capsys):
    content = (
        "a,b\n"
        "foo,1e1\n"
        "foo,\n"
        "bar,1e3\n"
        "baz,\n"
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(column="b", group_by=["a"])

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "bar,1e3\r\n"
        "foo,1e1\r\n"
    )
