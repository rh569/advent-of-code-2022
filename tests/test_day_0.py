import pytest

import days.day_0 as day

@pytest.mark.xfail
def test_part_1():
    assert day.part_1() == 42

def test_part_2():
    assert day.part_2() == 'abc'
