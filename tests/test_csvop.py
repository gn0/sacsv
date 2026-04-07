import io
import pytest

import sacsv.csvop as m


def test_missing_input_var_raises(monkeypatch):
    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(
            result_var="x",
            input_var=["c"],
            func_def="lambda x: x",
        )


def test_existing_result_var_raises(monkeypatch):
    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(ValueError):
        m.main(
            result_var="b",
            input_var=["a"],
            func_def="lambda x: x",
        )


def test_multiple_input_vars(monkeypatch, capsys):
    content = "a,b\n1,2\n3,4\n5,6\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        result_var="c",
        input_var=["a", "b"],
        func_def="lambda x, y: int(x) + int(y)",
    )

    assert (
        capsys.readouterr().out
        == "a,b,c\r\n1,2,3\r\n3,4,7\r\n5,6,11\r\n"
    )


def test_module_import(monkeypatch, capsys):
    content = "a\n10\n15\n20\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main(
        import_mod=["math"],
        result_var="b",
        input_var=["a"],
        func_def="lambda x: math.isqrt(int(x))",
    )

    assert capsys.readouterr().out == "a,b\r\n10,3\r\n15,3\r\n20,4\r\n"
