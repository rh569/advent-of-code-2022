DIRECTIONS = ['N', 'S', 'W', 'E']

class Neighbours():
    def __init__(self, elf, elves):
        i, j = elf

        self.n = [i - 1, j] in elves
        self.ne = [i - 1, j + 1] in elves
        self.e = [i, j + 1] in elves
        self.se = [i + 1, j + 1] in elves
        self.s = [i + 1, j] in elves
        self.sw = [i + 1, j - 1] in elves
        self.w = [i, j - 1] in elves
        self.nw = [i - 1, j - 1] in elves

        self.count = len([b for b in [
            self.n,
            self.ne,
            self.e,
            self.se,
            self.s,
            self.sw,
            self.w,
            self.nw
        ] if b])


def get_elves(input_path):
    with open(input_path) as input:
        lines = input.read().split('\n')

        elves = []

        for i, l in enumerate(lines):
            for j, c in enumerate(l):
                if c == '#':
                    elves.append([i, j])

        return elves


def print_elves(elves):
    print()
    min_i, max_i, min_j, max_j = get_bounds(elves)

    i_transform = -1 * min_i
    j_transform = -1 * min_j

    for _i in range(max_i + i_transform + 1):
        row = []
        for _j in range(max_j + j_transform + 1):
            i = _i - i_transform
            j = _j - j_transform

            if [i,j] in elves:
                row.append('#')
            else:
                row.append('.')
        print(row)
    print('   ~~~   ')


def do_round(elves, initial_dir_index):
    # first half
    proposed = []
    moved = 0

    for elf in elves:
        i, j = elf
        neighbours = Neighbours(elf, elves)

        if neighbours.count == 0:
            proposed.append(elf)
        else:
            found_proposal = False
            for dir_offset in range(len(DIRECTIONS)):
                d_index = (initial_dir_index + dir_offset) % len(DIRECTIONS)
                dir = DIRECTIONS[d_index]

                if dir == 'N':
                    if not neighbours.nw and not neighbours.n and not neighbours.ne:
                        proposed.append([i - 1, j])
                        found_proposal = True
                        break
                if dir == 'E':
                    if not neighbours.ne and not neighbours.e and not neighbours.se:
                        proposed.append([i, j + 1])
                        found_proposal = True
                        break
                if dir == 'S':
                    if not neighbours.se and not neighbours.s and not neighbours.sw:
                        proposed.append([i + 1, j])
                        found_proposal = True
                        break
                if dir == 'W':
                    if not neighbours.sw and not neighbours.w and not neighbours.nw:
                        proposed.append([i, j - 1])
                        found_proposal = True
                        break
            
            if not found_proposal:
                proposed.append(elf)

    # second half
    assert len(proposed) == len(elves)

    duplicate_indices = get_duplicate_proposal_indices(proposed)

    for p_index in duplicate_indices:
        proposed[p_index] = elves[p_index]

    for i, e in enumerate(elves):
        if e != proposed[i]:
            moved += 1

    return (proposed, moved == 0)


def get_duplicate_proposal_indices(proposed):
    duplicate_indices = []
    indices_by_pos = {}

    for i, p in enumerate(proposed):
        indices_for_p = indices_by_pos.get(f'{p}', [])
        indices_for_p.append(i)
        indices_by_pos[f'{p}'] = indices_for_p

    for v in indices_by_pos.values():
        if len(v) > 1:
            duplicate_indices.extend(v)

    return duplicate_indices


def get_bounds(elves) -> tuple[int, int, int, int]:
    i_s = [elf[0] for elf in elves]
    j_s = [elf[1] for elf in elves]

    return (min(i_s), max(i_s), min(j_s), max(j_s))


def part_1(input_path="input/day_23.txt"):
    elves = get_elves(input_path)

    dir_index = 0

    for _ in range(10):
        elves, _ = do_round(elves, dir_index)
        dir_index = (dir_index + 1) % len(DIRECTIONS)

    min_i, max_i, min_j, max_j = get_bounds(elves)

    return ((max_i - min_i + 1) * (max_j - min_j + 1)) - len(elves)


def part_2(input_path="input/day_23.txt"):
    elves = get_elves(input_path)

    dir_index = 0
    done = False
    round = 0

    while not done:
        # takes many minutes...
        elves, done = do_round(elves, dir_index)
        dir_index = (dir_index + 1) % len(DIRECTIONS)
        round += 1

    return round
