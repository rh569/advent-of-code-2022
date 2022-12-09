Pos = tuple[int, int]


def get_moves(input_path):
    """
    Returns a list of (i, j) tuples
    """
    with open(input_path) as input:
        lines = input.read().split('\n')

        moves: list[Pos] = []

        for l in lines:
            dir, n = l.split(' ')

            if dir == 'U':
                move = (-1, 0)
            elif dir == 'D':
                move = (1, 0)
            elif dir == 'L':
                move = (0, -1)
            else: # R
                move = (0, 1)
            
            for _ in range(int(n)):
                moves.append(move)
        
        return moves


def add_pos(p1: Pos, p2: Pos) -> Pos:
    return (p1[0] + p2[0], p1[1] + p2[1])


def sub_pos(p1: Pos, p2: Pos) -> Pos:
    return (p1[0] - p2[0], p1[1] - p2[1])


def reduce(p: Pos) -> Pos:
    """
    Reduces a given distance to a king's chess piece move
    i.e., (-2,1) -> (-1,1)
    """
    i, j = p

    if abs(i) > 1:
        i = i // 2
    
    if abs(j) > 1:
        j = j // 2
    
    return (i, j)


def propagate(k1: Pos, k2: Pos):
    diff = sub_pos(k1, k2)

    if (abs(diff[0]) > 1 or abs(diff[1]) > 1):
        move = reduce(diff)
        k2 = add_pos(k2, move)
    
    return k2


def part_1(input_path="input/day_9.txt"):
    moves = get_moves(input_path)

    visited: set[str] = set()
    
    h = (0, 0)
    t = (0, 0)
    visited.add(str(t))

    for m in moves:
        h = add_pos(h, m)
        t = propagate(h, t)
        visited.add(str(t))

    return len(visited)


def part_2(input_path="input/day_9.txt"):
    moves = get_moves(input_path)

    visited: set[str] = set()
    knots: list[Pos] = []

    for _ in range(10):
        knots.append((0, 0))

    visited.add(str(knots[9]))

    for m in moves:
        knots[0] = add_pos(knots[0], m)

        for i, k in enumerate(knots):
            if i == 0:
                continue
            
            knots[i] = propagate(knots[i-1], k)
        
        visited.add(str(knots[9]))

    return len(visited)
