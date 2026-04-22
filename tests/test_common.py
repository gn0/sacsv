import math

import sacsv as m


def test_try_cast_of_integer():
    assert m.try_cast("1") == 1
    assert m.try_cast("-1") == -1


def test_try_cast_of_float():
    assert m.try_cast("1.") == 1.0
    assert m.try_cast("-1.") == -1.0
    assert m.try_cast(".1") == 0.1
    assert m.try_cast("-.1") == -0.1
    assert m.try_cast("1e5") == 1e5
    assert m.try_cast("1e-5") == 1e-5
    assert m.try_cast("inf") == math.inf
    assert m.try_cast("-inf") == -math.inf
    assert math.isnan(m.try_cast("nan"))


def test_try_cast_of_empty_string():
    assert math.isnan(m.try_cast(""))


def test_try_cast_of_non_number():
    for x in (".", "-", "+", "0f", "foo"):
        assert m.try_cast(x) == x
