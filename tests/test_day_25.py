import pytest

import days.day_25 as day


test_input = "input/day_25_test.txt"
input = "input/day_25.txt"


@pytest.mark.parametrize(
    "dec,target",
    [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (11, "21"),
        (12, "22"),
        (13, "1=="),
        (14, "1=-"),
        (15, "1=0"),
        (16, "1=1"),
        (17, "1=2"),
        (18, "1-="),
        (19, "1--"),
        (20, "1-0"),
        (21, "1-1"),
        (22, "1-2"),
        (23, "10="),
        (24, "10-"),
        (25, "100"),
        # --
        (37, "122"),
        (38, "2=="),
        (61, "221"),
        (61, "221"),
    ],
)
def test_snafuise(dec, target):
    assert day.snafuise(dec) == target


def test_part_1():
    assert day.part_1(test_input) == "2=-1=0"
