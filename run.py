import sys
from time import process_time

from days import day_0, day_1, day_2, day_3, day_4, day_5, day_6, day_7, day_8, day_9, day_10, day_11, day_12, day_13, day_14, day_15, day_17, day_18, day_19

if __name__ != '__main__':
    sys.exit()

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
    day_12,
    day_13,
    day_14,
    day_15,
    day_15, # TODO replace with 16 (keeps index in line with day)
    day_17,
    day_18,
    day_19,
]


def run_day(i):
    print(f'~~ Day {i} ~~')

    try:
        print(f'  Part 1:')
        start_one = process_time()
        print(f'    {ALL_DAYS[i].part_1()}')
        elapsed_one = process_time() - start_one
        print(f'    {round(elapsed_one * 1000, 2)} ms')
    except AttributeError as e:
        print(f'    Failed to execute Day {i}: Part 1. Was it defined?')
        print(e.__cause__)

    try:
        print(f'  Part 2:')
        start_two = process_time()
        print(f'    {ALL_DAYS[i].part_2()}')
        elapsed_two = process_time() - start_two
        print(f'    {round(elapsed_two * 1000, 2)} ms')
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
