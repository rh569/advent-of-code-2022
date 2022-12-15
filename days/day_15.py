import re

def get_sensors(input_path):
    with open(input_path) as input:
        return [list(map(int,re.findall(r'\-?\d+', line))) for line in input.read().split('\n')]


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def condense_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges.sort(key=lambda r: r[1])
    ranges.sort(key=lambda r: r[0])

    condensed = []

    for r in ranges:
        if len(condensed) == 0:
            condensed.append(r)
        else:
            latest = condensed.pop()

            if r[0] <= latest[1]:
                latest = (latest[0], max(r[1], latest[1]))
                condensed.append(latest)
            else:
                condensed.append(latest)
                condensed.append(r)

    return condensed


def part_1(input_path="input/day_15.txt", target_y=2000000):
    sensors = get_sensors(input_path)

    x_in_target_y = set()
    b_in_target_y = set()

    for sensor in sensors:
        xs, ys, xb, yb = sensor

        if yb == target_y:
            b_in_target_y.add(xb)

        s_b_distance = get_distance([xs, ys], [xb, yb])
        s_target_distance = abs(target_y - ys)
        remaining_distance = s_b_distance - s_target_distance

        if remaining_distance >= 0:
            x_in_target_y.update(range(xs - remaining_distance, xs + remaining_distance + 1))

    return len(x_in_target_y.difference(b_in_target_y))


def part_2(input_path="input/day_15.txt", bound=4000000):
    sensors = get_sensors(input_path)

    for sensor in sensors:
        xs, ys, xb, yb = sensor

        s_b_distance = get_distance([xs, ys], [xb, yb])
        sensor.append(s_b_distance)
    
    for target_y in range(bound):
        x_ranges = []

        for sensor in sensors:
            xs, ys, xb, yb, d = sensor

            s_target_distance = abs(target_y - ys)
            remaining_distance = d - s_target_distance

            if remaining_distance >= 0:
                x_ranges.append((
                    max(xs - remaining_distance, 0),
                    min(xs + remaining_distance, bound)
                ))
        
        non_overlapping_ranges = condense_ranges(x_ranges)

        if len(non_overlapping_ranges) > 1:
            return (non_overlapping_ranges[0][1] + 1) * 4000000 + target_y
        
        if len(non_overlapping_ranges) == 1:
            span = abs(non_overlapping_ranges[0][1] - non_overlapping_ranges[0][0])
            if span < bound:
                raise RuntimeError("Not implemented")
        
    raise RuntimeError('Not Found')
