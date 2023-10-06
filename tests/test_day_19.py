import pytest

import days.day_19 as day


test_input = "input/day_19_test.txt"


def test_part_1():
    assert day.part_1(test_input) == 33


def test_part_2():
    assert day.part_2(test_input) == 3472
