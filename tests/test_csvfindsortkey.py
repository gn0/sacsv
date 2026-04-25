import io
import sys
import pytest

import sacsv.csvfindsortkey as m


def test_not_sorted(monkeypatch, capsys):
    content = "a,b\n1,a\n3,c\n2,b\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    m.main()

    assert capsys.readouterr().out == ""


def test_sorted_by_string(monkeypatch, capsys):
    for (a, b, c) in [
        ("1", "a", "b"),
        ("b", "a", "1"),
    ]:
        print(f"{a=} {b=} {c=}", file=sys.stderr)

        # Sorted.
        #

        content = (
            "a,b\n"
            f"1,{a}\n"
            f"3,{b}\n"
            f"2,{c}\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        with pytest.raises(SystemExit) as exception:
            m.main()

        assert exception.value.code == 0
        assert capsys.readouterr().out == "b\n"

        # Not sorted.
        #

        content = (
            "a,b\n"
            f"1,{a}\n"
            f"3,{c}\n"
            f"2,{b}\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        m.main()

        assert capsys.readouterr().out == ""


def test_sorted_by_int(monkeypatch, capsys):
    # Ascending.
    #

    content = "a,b\n1,a\n2,c\n3,b\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(SystemExit) as exception:
        m.main()

    assert exception.value.code == 0
    assert capsys.readouterr().out == "a\n"

    # Descending.
    #

    content = "a,b\n-1,a\n-2,c\n-3,b\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(content))

    with pytest.raises(SystemExit) as exception:
        m.main()

    assert exception.value.code == 0
    assert capsys.readouterr().out == "a\n"


def test_bigint(monkeypatch, capsys):
    # If large integers were parsed into a `float` rather than an `int`
    # (which is a bigint in Python 3), then these numbers would all be
    # treated as equal to each other and so these test cases would all
    # be inferred as sorted.
    #

    for (a, b, c) in [
        ("36893488147419103232",  # 2**65
         "36893488147419103233",  # 2**65 + 1
         "36893488147419103234"), # 2**65 + 2
        ("36893488147419103234",  # 2**65 + 2
         "36893488147419103233",  # 2**65 + 1
         "36893488147419103232"), # 2**65
    ]:
        print(f"{a=} {b=} {c=}", file=sys.stderr)

        # Sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{b},c\n"
            f"{c},b\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        with pytest.raises(SystemExit) as exception:
            m.main()

        assert exception.value.code == 0
        assert capsys.readouterr().out == "a\n"

        # Not sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{c},c\n"
            f"{b},b\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        m.main()

        assert capsys.readouterr().out == ""


def test_sorted_by_float(monkeypatch, capsys):
    for (a, b, c) in [
        ("1e1", "1e2", "1e3"),
        ("1e3", "1e2", "1e1"),
        ("1e-1", "1e-2", "1e-3"),
        ("1e-3", "1e-2", "1e-1"),
        ("1.2e2", "1.5e1", "0"),
        ("-inf", "0", "inf"),
        (".1", ".01", ".001"),
        ("-.1", "-.01", "-.001"),
    ]:
        print(f"{a=} {b=} {c=}", file=sys.stderr)

        # Sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{b},c\n"
            f"{c},b\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        with pytest.raises(SystemExit) as exception:
            m.main()

        assert exception.value.code == 0
        assert capsys.readouterr().out == "a\n"

        # Not sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{c},c\n"
            f"{b},b\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        m.main()

        assert capsys.readouterr().out == ""


def test_missing_values(monkeypatch, capsys):
    for (a, b, c, d) in [
        ("11.0", "", "2.0", "1.0"),
        ("1.0", "", "2.0", "11.0"),
        ("1", "", "3", "4"),
        ("a", "", "c", "d"),
    ]:
        print(f"{a=} {b=} {c=}", file=sys.stderr)

        # Sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{b},c\n"
            f"{c},b\n"
            f"{d},d\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        with pytest.raises(SystemExit) as exception:
            m.main()

        assert exception.value.code == 0
        assert capsys.readouterr().out == "a\n"

        # Not sorted.
        #

        content = (
            "a,b\n"
            f"{a},a\n"
            f"{d},c\n"
            f"{b},b\n"
            f"{c},d\n"
        )
        monkeypatch.setattr("sys.stdin", io.StringIO(content))

        m.main()

        assert capsys.readouterr().out == ""
