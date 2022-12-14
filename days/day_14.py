def get_rock_paths(input_path):
    with open(input_path) as input:
        rock_paths = [line.split(' -> ') for line in input.read().split('\n')]
        rock_paths = [[list(map(int, coord.split(','))) for coord in path] for path in rock_paths]
        return rock_paths


def get_rocks(rock_path: list[list[int]]) -> list[list[int]]:
    rocks = []

    for i, p1 in enumerate(rock_path):
        if i == len(rock_path) - 1: continue
        p2 = rock_path[i + 1]

        # vertical lines
        if p1[0] == p2[0] and p1[1] < p2[1]:
            for y in range(p1[1], p2[1] + 1):
                rocks.append([p1[0], y])
        if p1[0] == p2[0] and p1[1] > p2[1]:
            for y in range(p2[1], p1[1] + 1):
                rocks.append([p1[0], y])
        
        # horizontal lines
        if p1[1] == p2[1] and p1[0] < p2[0]:
            for x in range(p1[0], p2[0] + 1):
                rocks.append([x, p1[1]])
        if p1[1] == p2[1] and p1[0] > p2[0]:
            for x in range(p2[0], p1[0] + 1):
                rocks.append([x, p1[1]])
    
    return rocks


def make_rocks_by_x_map(rock_paths: list[list[list[int]]]):
    rocks_by_x: dict[int, list[int]] = {}

    for p in rock_paths:
        for r in get_rocks(p):
            if rocks_by_x.get(r[0]) is None:
                rocks_by_x[r[0]] = [r[1]]
            elif not r[1] in rocks_by_x[r[0]]:
                rocks_by_x[r[0]].append(r[1])
    
    return rocks_by_x


def pour_sand(rocks_by_x: dict[int, list[int]], consider_floor: bool = False) -> int:
    n_settled = 0

    greatest_y = 0
    for ys in rocks_by_x.values():
        for y in ys:
            greatest_y = max(greatest_y, y)
    
    if consider_floor:
        greatest_y += 2

        # add in the floor - sand can reach at most greatest_y in each direction
        for x in range(500 - greatest_y, 500 + greatest_y + 1):
            if rocks_by_x.get(x) is None:
                rocks_by_x[x] = [greatest_y]
            else:
                rocks_by_x[x].append(greatest_y)

    sand_x = 500
    sand_y = 0

    # if sand_y goes beyond the furthest y, it will fall forever
    while sand_y <= greatest_y:
        # fall down
        if not sand_y + 1 in rocks_by_x.get(sand_x, []):
            sand_y += 1
        # fall left
        elif not sand_y + 1 in rocks_by_x.get(sand_x - 1, []):
            sand_x -= 1
            sand_y += 1
        # fall right
        elif not sand_y + 1 in rocks_by_x.get(sand_x + 1, []):
            sand_x += 1
            sand_y += 1
        # settle (become a rock)
        else:
            if rocks_by_x.get(sand_x) is None:
                rocks_by_x[sand_x] = [sand_y]
            else:
                rocks_by_x[sand_x].append(sand_y)
            n_settled += 1

            if sand_x == 500 and sand_y == 0:
                return n_settled

            sand_x = 500
            sand_y = 0
        
    return n_settled


def part_1(input_path="input/day_14.txt"):
    paths = get_rock_paths(input_path)
    rocks_by_x = make_rocks_by_x_map(paths)

    return pour_sand(rocks_by_x)


def part_2(input_path="input/day_14.txt"):
    paths = get_rock_paths(input_path)
    rocks_by_x = make_rocks_by_x_map(paths)

    return pour_sand(rocks_by_x, True)
