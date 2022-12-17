def get_jets(input_path):
    with open(input_path) as input:
        return list(input.read().strip())

get_hero = lambda: [
    [1,0,0,0],
    [1,0,0,0],
    [1,0,0,0],
    [1,0,0,0],
]

get_smashboy = lambda: [
    [0,0,0,0],
    [0,0,0,0],
    [1,1,0,0],
    [1,1,0,0],
]

get_teewee_plus = lambda: [
    [0,0,0,0],
    [0,1,0,0],
    [1,1,1,0],
    [0,1,0,0],
]

get_long_ricky = lambda: [
    [0,0,0,0],
    [0,0,1,0],
    [0,0,1,0],
    [1,1,1,0],
]

get_zero = lambda: [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [1,1,1,1],
]

FALL_ORDER = [
    get_zero, get_teewee_plus, get_long_ricky, get_hero, get_smashboy
]

get_row = lambda: [2,0,0,0,0,0,0,0,2]


def add_rows(cave, n_rows):
    for _ in range(n_rows):
        cave.insert(0, get_row())


def make_cave():
    cave = [
        [2,2,2,2,2,2,2,2,2]
    ]

    add_rows(cave, 7)
    
    return cave


def increase_cave_height(cave):
    """
    Finds highest rock height and ensures 4 rows above that
    """
    first_rock_row = -1
    head_room_required = 7

    for i, row in enumerate(cave):
        mid = row[1:-1]
        
        if 1 in mid:
            first_rock_row = i
            break
    
    if first_rock_row < head_room_required:
        n = head_room_required - first_rock_row
        add_rows(cave, n)


def get_floor_pattern(cave):
    pattern = []

    for j in range(1,8):
        for i, row in enumerate(cave):
            if row[j] > 0:
                pattern.append(i)
                break

    smallest = pattern[0]

    for p in pattern:
        smallest = min(p, smallest)

    pattern = [p - smallest for p in pattern]

    return pattern


def get_largest_pattern_gap(pattern):
    largest_gap = 0

    for i, p1 in enumerate(pattern[:-1]):
        p2 = pattern[i + 1]
        largest_gap = max(abs(p2 - p1), largest_gap)
    
    return largest_gap


def is_collision(r, r_pos, c):
    is_collision = False

    for i, r_row in enumerate(r):
        for j, r_cell in enumerate(r_row):
            if r_cell == 1:
                # -3 handles the local origin of the rocks as bottom left
                c_pos = [r_pos[0] + i - 3, r_pos[1] + j]

                if c[c_pos[0]][c_pos[1]] != 0:
                    is_collision = True

    return is_collision


def drop_rock(rock_index, jets, jet_index, cave):
    rock = FALL_ORDER[rock_index]()
    rock_index = (rock_index + 1) % len(FALL_ORDER)

    # global (cave) i, j (defines lower left of rock)
    rock_pos = [3, 3]
    falling = True
    next_move = 'jet'

    while falling:
        test_pos = rock_pos[:]

        if next_move == 'jet':
            if jets[jet_index] == '>':
                test_pos[1] += 1
            else:
                test_pos[1] -= 1

            jet_index = (jet_index + 1) % len(jets)

            if not is_collision(rock, test_pos, cave):
                rock_pos = test_pos

            next_move = 'fall'
        elif next_move == 'fall':
            test_pos[0] += 1

            if is_collision(rock, test_pos, cave):
                place_rock(rock, rock_pos, cave)
                increase_cave_height(cave)
                falling = False
            else:
                rock_pos = test_pos

            next_move = 'jet'
    
    return rock_index, jet_index


def place_rock(r, r_pos, c):
    c_updates = []

    # plan placement
    for i, r_row in enumerate(r):
        for j, r_cell in enumerate(r_row):
            if r_cell == 1:
                # -3 handles the local origin of the rocks as bottom left
                c_pos = [r_pos[0] + i - 3, r_pos[1] + j]
                if c[c_pos[0]][c_pos[1]] != 0:
                    raise RuntimeError(f'Cannot place rock at {r_pos} in {print_cave(c)}')
                else:
                    c_updates.append(c_pos)
    
    # do placement
    for i, j in c_updates:
        c[i][j] = 1


def get_height_of_rocks(cave):
    return len(cave) - 1 - 7


def print_cave(cave, n=None):
    print()

    if n is None:
        _cave = cave
    else:
        _cave = cave[4:n+4]

    for r in _cave:
        row = "".join(
            [['.','@','#'][cell] for cell in r]
        )
        print(row)
    
    if n is not None:
        print('~~~~~~~~~')


def part_1(input_path="input/day_17.txt"):
    jets = get_jets(input_path)

    cave = make_cave()

    rock_index = 0
    jet_index = 0

    for _ in range(2022):
        rock_index, jet_index = drop_rock(rock_index, jets, jet_index, cave)

    return get_height_of_rocks(cave)


def part_2(input_path="input/day_17.txt"):
    jets = get_jets(input_path)
    cave = make_cave()

    # list of floor patterns, by jet index, by rock index
    known_patterns = [
        [], # rock 0
        [], # rock 1
        [], # etc.
        [],
        [],
    ]

    for row in known_patterns:
        for _ in range(len(jets)):
            row.append([])

    rock_index = 0
    jet_index = 0

    found_repeat = False
    height_to_repeat_end = -1
    height_repeat_found = -1
    stop_after = -1

    try_n_rocks = 10000

    for rr in range(try_n_rocks):
        current_pattern = get_floor_pattern(cave)

        # Prevent edge case where rocks slipping through sidewards can break the repeat
        # For given input any value up to about 20 actually works
        if get_largest_pattern_gap(current_pattern) <= 2:
            patterns_for_rock_and_jet = [p_obj['p'] for p_obj in known_patterns[rock_index][jet_index]]

            if not found_repeat and current_pattern in patterns_for_rock_and_jet:
                index = patterns_for_rock_and_jet.index(current_pattern)
                old_pattern = known_patterns[rock_index][jet_index][index]
                found_repeat = True
                
                height_repeat_found = get_height_of_rocks(cave)

                repeat_length_rocks = rr - old_pattern['at']
                remaining_rocks_to_fall = (1000000000000 - old_pattern['at']) % repeat_length_rocks
                stop_after = rr + remaining_rocks_to_fall

                n_reps = (1000000000000 - old_pattern['at']) // repeat_length_rocks
                repeat_height = height_repeat_found - old_pattern['height']
                height_to_repeat_end = old_pattern['height'] + n_reps * repeat_height

            elif not found_repeat:
                known_patterns[rock_index][jet_index].append(
                    {
                        'p': current_pattern,
                        'height': get_height_of_rocks(cave),
                        'at': rr
                    }
                )

        rock_index, jet_index = drop_rock(rock_index, jets, jet_index, cave)

        if found_repeat and rr == stop_after - 1:
            end_height = get_height_of_rocks(cave) - height_repeat_found
            return height_to_repeat_end + end_height

    raise RuntimeError(f"Didn't find a repeat in {try_n_rocks} rocks")
