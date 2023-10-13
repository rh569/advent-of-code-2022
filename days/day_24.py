class Blizzard:
    def __init__(self, pos: tuple[int, int], dir: tuple[int, int]) -> None:
        self.pos = pos
        self.dir = dir


def get_valley_input(input_path) -> tuple[int, int, list[Blizzard]]:
    with open(input_path) as input:
        lines = input.read().split('\n')

        height = len(lines)
        width = len(lines[0])
        blizzards = []

        for i, chars in enumerate(lines):
            for j, c in enumerate(chars):
                if c == '>':
                    blizzards.append(Blizzard((i, j), (0, 1)))
                if c == 'v':
                    blizzards.append(Blizzard((i, j), (1, 0)))
                if c == '<':
                    blizzards.append(Blizzard((i, j), (0, -1)))
                if c == '^':
                    blizzards.append(Blizzard((i, j), (-1, 0)))
        
        return (height, width, blizzards)


def advance_blizzards(height: int, width: int, blizzards: list[Blizzard]) -> None:
    for b in blizzards:
        i, j = b.pos
        
        if b.dir == (0, 1):
            if j + 1 <= width - 2:
                b.pos = (i, j+1)
            else:
                b.pos = (i, 1)
        
        if b.dir == (1, 0):
            if i + 1 <= height - 2:
                b.pos = (i+1, j)
            else:
                b.pos = (1, j)
        
        if b.dir == (0, -1):
            if j - 1 >= 1:
                b.pos = (i, j-1)
            else:
                b.pos = (i, width - 2)
        
        if b.dir == (-1, 0):
            if i - 1 >= 1:
                b.pos = (i-1, j)
            else:
                b.pos = (height - 2, j)


def get_neighbours(pos: tuple[int, int], height: int, width: int) -> list[tuple[int, int]]:
    n = []

    for i in [-1, 1]:
        new_i = pos[0] + i

        if ((new_i >= 1 and new_i <= height - 2) or
            (new_i == 0 and pos[1] == 1) or (new_i == height - 1 and pos[1] == width - 2)):
            n.append((new_i, pos[1]))

    for j in [-1, 1]:
        new_j = pos[1] + j

        if new_j >= 1 and new_j <= width - 2 and pos[0] >= 1 and pos[0] <= height - 2:
            n.append((pos[0], new_j))

    return n


def part_1(input_path="input/day_24.txt"):
    height, width, blizzards = get_valley_input(input_path)

    pos = (0, 1)
    end = (height - 1, width - 2)

    possible_paths: list[list[tuple[int, int]]] = [
        [pos]
    ]

    run_time = 500

    for minute in range(run_time):
        next_minute_possible_paths = []
        # print(f'Found {len(possible_paths)} paths after {minute} mins')

        advance_blizzards(height, width, blizzards)
        blizzard_possitions = [b.pos for b in blizzards]

        while len(possible_paths) > 0:

            current_path = possible_paths.pop()
            current_pos = current_path[-1]
            new_paths = []

            if current_pos not in blizzard_possitions:
                new_path = current_path[:]
                new_path.append(current_pos)
                new_paths.append(new_path)

            neighbours = get_neighbours(current_pos, height, width)

            for n in neighbours:
                if n not in blizzard_possitions:
                    new_path = current_path[:]
                    new_path.append(n)

                    if n == end:
                        return len(current_path)
                    else:
                        new_paths.append(new_path)
            
            next_minute_possible_paths.extend(new_paths)
        
        unique_positions = []

        # Actual route doesn't matter - only care about position at each minute
        for path in next_minute_possible_paths:
            if not path[-1] in unique_positions:
                possible_paths.append(path)
                unique_positions.append(path[-1])

    raise RuntimeError(f'No path found in {run_time} minutes')


def part_2(input_path="input/day_24.txt"):
    height, width, blizzards = get_valley_input(input_path)

    pos = (0, 1)

    targets = [
        (height - 1, width - 2),
        (0, 1),
        (height - 1, width - 2),
    ]

    target_idx = 0
    target_reached = False

    possible_paths: list[list[tuple[int, int]]] = [
        [pos]
    ]

    run_time = 1500

    for minute in range(run_time):
        next_minute_possible_paths = []
        # print(f'Found {len(possible_paths)} paths after {minute} mins')

        advance_blizzards(height, width, blizzards)
        blizzard_possitions = [b.pos for b in blizzards]

        while len(possible_paths) > 0:

            current_path = possible_paths.pop()
            current_pos = current_path[-1]
            new_paths = []

            if current_pos not in blizzard_possitions:
                new_path = current_path[:]
                new_path.append(current_pos)
                new_paths.append(new_path)

            neighbours = get_neighbours(current_pos, height, width)

            for n in neighbours:
                if n not in blizzard_possitions:
                    new_path = current_path[:]
                    new_path.append(n)

                    if n == targets[target_idx]:
                        target_reached = True
                        break
                    else:
                        new_paths.append(new_path)
            
            next_minute_possible_paths.extend(new_paths)
        
        if not target_reached:
            unique_positions = []

            # Actual route doesn't matter - only care about position at each minute
            for path in next_minute_possible_paths:
                if not path[-1] in unique_positions:
                    possible_paths.append(path)
                    unique_positions.append(path[-1])
        else:
            if target_idx == len(targets) - 1:
                return minute + 1
            else:
                possible_paths = [[targets[target_idx]]]
                target_reached = False
                target_idx += 1

    raise RuntimeError(f'No path found in {run_time} minutes')
