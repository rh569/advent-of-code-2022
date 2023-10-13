import pytest

import days.day_21 as day


test_input = "input/day_21_test.txt"


def test_part_1():
    assert day.part_1(test_input) == 152


def test_part_2():
    assert day.part_2(test_input) == 301
