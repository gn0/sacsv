import sacsv.csvappend as m


def test_union_of_input_fieldnames():
    cases = [
        ((["a", "b"], ["a"]), ["a", "b"]),
        ((["a", "b"], ["b"]), ["a", "b"]),
        ((["a", "b"], ["a", "b"]), ["a", "b"]),
        ((["a", "b"], ["b", "a"]), ["a", "b"]),
        ((["a", "b"], ["a", "b", "c"]), ["a", "b", "c"]),
        ((["a", "b"], ["c"]), ["a", "b", "c"]),
        ((["a", "b"], ["c", "d"]), ["a", "b", "c", "d"]),
        ((["a", "b"], ["c", "d", "e"]), ["a", "b", "c", "d", "e"]),
    ]
    for arg, expected in cases:
        assert m.get_fieldnames(arg) == expected


def test_field_getter():
    assert m.make_get_fields("a", "b")({"a": 3}) == (3, None)
    assert m.make_get_fields("a", "b")({"b": 2}) == (None, 2)
    assert m.make_get_fields("a", "b")({"c": 1}) == (None, None)
    assert m.make_get_fields("a", "b")({"a": 3, "b": 2}) == (3, 2)
