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
