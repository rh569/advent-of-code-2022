import pytest

import days.day_12 as day


test_input = "input/day_12_test.txt"


def test_part_1():
    assert day.part_1(test_input) == 31

# This just happens to pass...
# It would fail if the best route was from (0, 1)
def test_part_2():
    assert day.part_2(test_input) == 29
