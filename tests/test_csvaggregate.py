import io
import pytest

import sacsv.csvaggregate as m


def test_missing_column_raises(monkeypatch):
    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(
            columns=["x"],
            func_def="lambda x: x",
        )

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(
            columns=["x"],
            group_by=["a"],
            func_def="lambda x: x",
        )

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(
            columns=["a"],
            group_by=["x"],
            func_def="lambda x: x",
        )


def test_multiple_columns(monkeypatch, capsys):
    # Applying function to multiple columns.
    #

    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        columns=["a", "b"],
        func_def="lambda x: sum(map(int, x))",
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "9,12\r\n"
    )

    # Grouping by multiple columns.
    #

    content = "a,b,c\n1,1,2\n1,1,3\n1,2,5\n1,2,7\n1,3,11\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        columns=["c"],
        group_by=["a", "b"],
        func_def="lambda x: sum(map(int, x))",
    )

    assert capsys.readouterr().out == (
        "a,b,c\r\n"
        "1,1,5\r\n"
        "1,2,12\r\n"
        "1,3,11\r\n"
    )


def test_module_import(monkeypatch, capsys):
    content = "a,b\n1,9\n1,16\n2,25\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        import_mod=["math"],
        columns=["b"],
        group_by=["a"],
        func_def="lambda x: sum(map(math.isqrt, map(int, x)))",
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,7\r\n"
        "2,5\r\n"
    )


def test_auto_cast(monkeypatch, capsys):
    # `sum` raises `TypeError` without `--auto-cast`.
    #

    content = "a,b\n1,9\n1,16\n2,25\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(TypeError):
        m.main(
            import_mod=["math"],
            columns=["b"],
            group_by=["a"],
            func_def="lambda x: sum(map(math.isqrt, x))",
        )

    assert capsys.readouterr().out == "a,b\r\n"

    # `sum` works with `--auto-cast`.
    #

    content = "a,b\n1,9\n1,16\n2,25\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        import_mod=["math"],
        columns=["b"],
        group_by=["a"],
        func_def="lambda x: sum(map(math.isqrt, x))",
        auto_cast=True,
    )

    assert capsys.readouterr().out == (
        "a,b\r\n"
        "1,7\r\n"
        "2,5\r\n"
    )
