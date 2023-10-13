import pytest

import days.day_20 as day


test_input = "input/day_20_test.txt"


def test_part_1():
    assert day.part_1(test_input) == 3


def test_part_2():
    assert day.part_2(test_input) == 1623178306
