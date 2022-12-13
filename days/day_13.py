import functools
import re

from typing import Optional


def get_pairs(input_path):
    with open(input_path) as input:
        return [pair.split('\n') for pair in input.read().split('\n\n')]


def get_packets(input_path):
    with open(input_path) as input:
        return [eval(s) for s in re.sub(r'\n\n', r'\n', input.read()).split('\n')]


def check_order(left, right) -> Optional[bool]:
    tl = type(left)
    tr = type(right)

    if tl is int and tr is int:
        if left < right: return True
        if left == right: return None
        if left > right: return False
    elif tl is list and tr is list:
        if len(left) == 0 and len(right) > 0:
            return True
        for i, xl in enumerate(left):
            if i >= len(right): return False
            check = check_order(xl, right[i])

            if check is True: return True
            if check is False: return False

            if check is None:
                if i == len(left) - 1 and len(left) < len(right):
                    return True
    elif tl is int:
        left = [left]
        return check_order(left, right)
    elif tr is int:
        right = [right]
        return check_order(left, right)
    else:
        raise RuntimeError(f'Not handled types: {tl} {tr}')


def wrapped_check_order(left, right) -> int:
    check = check_order(left, right)
    
    if check == True:
        return -1
    if check == False:
        return 1
    
    return 0


def part_1(input_path="input/day_13.txt"):
    pairs = get_pairs(input_path)

    indices = []

    for i, pair in enumerate(pairs):
        l = eval(pair[0])
        r = eval(pair[1])

        check = check_order(l, r)

        if check is True:
            indices.append(i+1)

    return sum(indices)


def part_2(input_path="input/day_13.txt"):
    packets = get_packets(input_path)
    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=functools.cmp_to_key(wrapped_check_order))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
