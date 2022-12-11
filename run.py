import sys

from days import day_0, day_1, day_2, day_3, day_4, day_5, day_6, day_7, day_8, day_9, day_10, day_11

if __name__ != 'main':
    pass

ALL_DAYS = [
    day_0,
    day_1,
    day_2,
    day_3,
    day_4,
    day_5,
    day_6,
    day_7,
    day_8,
    day_9,
    day_10,
    day_11,
]


def run_day(i):
    print(f'~~ Day {i} ~~')

    try:
        print(f'  Part 1:')
        print(f'    {ALL_DAYS[i].part_1()}')
    except AttributeError as e:
        print(f'    Failed to execute Day {i}: Part 1. Was it defined?')
        print(e.__cause__)

    try:
        print(f'  Part 2:')
        print(f'    {ALL_DAYS[i].part_2()}')
    except AttributeError as e:
        print(f'    Failed to execute Day {i}: Part 2. Was it defined?')
        print(e.__cause__)

    print()


def run_all_days():
    for i in range(len(ALL_DAYS)):
        run_day(i)

if (len(sys.argv) > 1 and
    sys.argv[1].isdigit()):

    run_day(int(sys.argv[1], 10))
else:
    run_all_days()
