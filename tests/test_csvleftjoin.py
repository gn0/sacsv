import io
import pytest
import unittest.mock as mock

import sacsv.csvleftjoin as m


def test_one_key(monkeypatch, capsys):
    join_content = "a,c\n1,foo\n5,bar\n7,baz\n"
    mopen = mock.mock_open(read_data=join_content)

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with mock.patch("builtins.open", mopen):
        m.main(
            join_table="foobar.csv",
            keys=["a"],
        )

    assert (
        capsys.readouterr().out
        == "a,b,c\r\n1,2,foo\r\n3,4,\r\n5,6,bar\r\n"
    )


def test_two_keys(monkeypatch, capsys):
    join_content = "a,b,c\n1,2,foo\n5,6,bar\n7,8,baz\n"
    mopen = mock.mock_open(read_data=join_content)

    content = "a,b,x\n1,2,lorem\n3,4,ipsum\n5,6,dolor\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with mock.patch("builtins.open", mopen):
        m.main(
            join_table="foobar.csv",
            keys=["a", "b"],
        )

    assert (
        capsys.readouterr().out
        == "a,b,x,c\r\n1,2,lorem,foo\r\n3,4,ipsum,\r\n5,6,dolor,bar\r\n"
    )


def test_key_missing_in_join(monkeypatch, capsys):
    join_content = "a,c\n1,foo\n5,bar\n7,baz\n"
    mopen = mock.mock_open(read_data=join_content)

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        with mock.patch("builtins.open", mopen):
            m.main(
                join_table="foobar.csv",
                keys=["b"],
            )


def test_key_missing_in_input(monkeypatch, capsys):
    join_content = "a,c\n1,foo\n5,bar\n7,baz\n"
    mopen = mock.mock_open(read_data=join_content)

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        with mock.patch("builtins.open", mopen):
            m.main(
                join_table="foobar.csv",
                keys=["c"],
            )


def test_1_to_n_match_yields_n_rows(monkeypatch, capsys):
    join_content = "a,c\n1,foo\n1,lorem\n5,bar\n7,baz\n"
    mopen = mock.mock_open(read_data=join_content)

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with mock.patch("builtins.open", mopen):
        m.main(
            join_table="foobar.csv",
            keys=["a"],
        )

    assert (
        capsys.readouterr().out
        == "a,b,c\r\n1,2,foo\r\n1,2,lorem\r\n3,4,\r\n5,6,bar\r\n"
    )
