import io

import sacsv.fw2csv as m


def test_single_line_stacks():
    assert (
        list(m.iter_stacks_of(1, "abcdef"))
        == [("a",), ("b",), ("c",), ("d",), ("e",), ("f",)]
    )


def test_triple_line_stacks_without_leftover():
    assert (
        list(m.iter_stacks_of(3, "abcdef"))
        == [("a", "b", "c"), ("d", "e", "f")]
    )


def test_triple_line_stacks_with_leftover():
    assert (
        list(m.iter_stacks_of(3, "abcdefg"))
        == [("a", "b", "c"), ("d", "e", "f"), ("g",)]
    )


def test_one_input_line_per_record(monkeypatch, capsys):
    content = (
        "   1   2   0\n"
        "   4   3   5\n"
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(lines_by_record=1, field=["1-4:foo", "5-8:bar", "9-12:baz"])

    assert capsys.readouterr().out == (
        "foo,bar,baz\r\n"
        "   1,   2,   0\r\n"
        "   4,   3,   5\r\n"
    )


def test_two_input_lines_per_record(monkeypatch, capsys):
    content = (
        "   1   2   0\n"
        "   4   3   5\n"
        "   7   2   5\n"
        "   0   3   7\n"
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        lines_by_record=2,
        field=[
            "1-4:foo",
            "5-8:bar",
            "9-12:baz",
            "2:1-4:lorem",
            "2:5-8:ipsum",
            "2:9-12:dolor",
        ],
    )

    assert capsys.readouterr().out == (
        "foo,bar,baz,lorem,ipsum,dolor\r\n"
        "   1,   2,   0,   4,   3,   5\r\n"
        "   7,   2,   5,   0,   3,   7\r\n"
    )
