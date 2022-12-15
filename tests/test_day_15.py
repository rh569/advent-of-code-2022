import days.day_15 as day


test_input = "input/day_15_test.txt"


def test_part_1():
    assert day.part_1(test_input, 10) == 26


def test_part_2():
    assert day.part_2(test_input, 20) == 56000011
