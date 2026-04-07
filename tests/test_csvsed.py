import io

import sacsv.csvsed as m


def test_one_column(monkeypatch, capsys):
    content = "a,b\nlorem,ipsum\ndolor,sit\namet,consectetuer\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        columns=["b"],
        pattern="[ps]",
        to="x",
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "lorem,ixxum\r\n"
        "dolor,xit\r\n"
        "amet,conxectetuer\r\n"
    )


def test_two_columns(monkeypatch, capsys):
    content = "a,b\nlorem,ipsum\ndolor,sit\namet,consectetuer\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        columns=["a", "b"],
        pattern="[ls]",
        to="x",
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "xorem,ipxum\r\n"
        "doxor,xit\r\n"
        "amet,conxectetuer\r\n"
    )


def test_group_in_replacement(monkeypatch, capsys):
    content = "a,b\nlorem,ipsum\ndolor,sit\namet,consectetuer\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        columns=["b"],
        pattern="([ps]+)",
        to=r"<\1>",
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "lorem,i<ps>um\r\n"
        "dolor,<s>it\r\n"
        "amet,con<s>ectetuer\r\n"
    )
