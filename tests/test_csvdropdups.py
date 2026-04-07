import io

import argh
import pytest

import sacsv.csvdropdups as m

CONTENT = (
    "a,b,c\r\n"
    "1,1,1\r\n"
    "1,1,2\r\n"
    "1,2,1\r\n"
    "1,2,2\r\n"
    "2,1,1\r\n"
    "2,1,2\r\n"
    "2,2,1\r\n"
    "2,2,2\r\n"
    "3,1,1\r\n"
)


def test_one_key(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(CONTENT))

    m.main(key=["a"], keep_first=["b", "c"])

    assert capsys.readouterr().out == (
        "a,b,c\r\n"
        "1,1,1\r\n"
        "2,1,1\r\n"
        "3,1,1\r\n"
    )

    monkeypatch.setattr("sys.stdin", io.StringIO(CONTENT))

    m.main(key=["a"], keep_last=["b", "c"])

    assert capsys.readouterr().out == (
        "a,b,c\r\n"
        "1,2,2\r\n"
        "2,2,2\r\n"
        "3,1,1\r\n"
    )


def test_two_keys(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(CONTENT))

    m.main(key=["a", "b"], keep_first=["c"])

    assert capsys.readouterr().out == (
        "a,b,c\r\n"
        "1,1,1\r\n"
        "1,2,1\r\n"
        "2,1,1\r\n"
        "2,2,1\r\n"
        "3,1,1\r\n"
    )

    monkeypatch.setattr("sys.stdin", io.StringIO(CONTENT))

    m.main(key=["a", "b"], keep_last=["c"])

    assert capsys.readouterr().out == (
        "a,b,c\r\n"
        "1,1,2\r\n"
        "1,2,2\r\n"
        "2,1,2\r\n"
        "2,2,2\r\n"
        "3,1,1\r\n"
    )


def test_must_specify_keep_first_xor_keep_last():
    with pytest.raises(argh.CommandError):
        m.main(key=["a"], keep_first=["b"], keep_last=["c"])

    with pytest.raises(argh.CommandError):
        m.main(key=["a"], keep_first=None, keep_last=None)
