import pytest

import days.day_3 as day

test_input = "input/day_3_test.txt"


def test_part_1():
    assert day.part_1(test_input) == 157


def test_part_2():
    assert day.part_2(test_input) == 70


@pytest.mark.parametrize('char, priority', [
    ('a', 1),
    ('z', 26),
    ('A', 27),
    ('Z', 52),
])
def test_get_priority(char, priority):
    assert day.get_priority(char) == priority
