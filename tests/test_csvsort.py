import io
import pytest

import sacsv.csvsort as m


def test_missing_column_raises(monkeypatch):
    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(columns=["x"], delimiter=",")

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(columns=["x"], delimiter=",", auto_cast=True)


def test_default_columns(monkeypatch, capsys):
    content = "a,b\n2,baz\n1,foo\n11,bar\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(columns=None, delimiter=",")

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,foo\r\n"
        "11,bar\r\n"
        "2,baz\r\n"
    )


def test_specific_columns(monkeypatch, capsys):
    content = "a,b\n2,baz\n1,foo\n1,asd\n11,bar\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(columns=["b"], delimiter=",")

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,asd\r\n"
        "11,bar\r\n"
        "2,baz\r\n"
        "1,foo\r\n"
    )

    content = "a,b\n2,baz\n1,foo\n1,asd\n11,bar\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(columns=["a", "b"], delimiter=",")

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,asd\r\n"
        "1,foo\r\n"
        "11,bar\r\n"
        "2,baz\r\n"
    )


def test_auto_cast(monkeypatch, capsys):
    content = "a,b\n2,baz\n1,foo\n1,asd\n11,bar\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(columns=["b"], delimiter=",", auto_cast=True)

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,asd\r\n"
        "11,bar\r\n"
        "2,baz\r\n"
        "1,foo\r\n"
    )

    content = "a,b\n2,baz\n1,foo\n1,asd\n11,bar\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(columns=["a", "b"], delimiter=",", auto_cast=True)

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,asd\r\n"
        "1,foo\r\n"
        "2,baz\r\n"
        "11,bar\r\n"
    )
