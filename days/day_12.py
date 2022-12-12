from typing import Optional


def get_height_map(input_path):
    with open(input_path) as input:
        return [list(l) for l in input.read().split('\n')]


Pos = tuple[int, int]
HeightMap = list[list[str]]
LetterPositions = dict[str, list[Pos]]


class Route():
    head: Pos
    visited: list[Pos]

    def __init__(self, head: Pos, visited: Optional[list[Pos]] = None):
        self.visited = [head] if visited is None else visited[:]
        self.head = head

    def move(self, p: Pos):
        self.head = p

        assert not p in self.visited
        self.visited.append(p)


def read_map(map: HeightMap) -> tuple[Pos, Pos, LetterPositions]:
    pos_by_letter: dict[str, list[Pos]] = dict([(x, []) for x in list('abcdefghijklmnopqrstuvwxyz')])
    start = None
    target = None

    for i, row in enumerate(map):
        for j, height in enumerate(row):
            if height == 'S':
                start = (i, j)
            elif height == 'E':
                target = (i, j)
            else:
                pos_by_letter[height].append((i, j))
    
    if start is not None and target is not None:
        return (start, target, pos_by_letter)
    
    raise


def get_neighbours(map: HeightMap, p: Pos) -> list[Pos]:
    i, j = p
    n = []

    if i + 1 < len(map):
        n.append((i+1, j))
    if i - 1 >= 0:
        n.append((i-1, j))
    if j + 1 < len(map[i]):
        n.append((i, j+1))
    if j - 1 >= 0:
        n.append((i, j-1))
    
    return n


def val(c: str) -> int:
    ab = list('abcdefghijklmnopqrstuvwxyz')

    if c == 'E':
        return ab.index('z')
    if c == 'S':
        return ab.index('a')

    return ab.index(c)


def find_shortest_route(height_map: HeightMap, start: Pos, target: Pos) -> Route:
    wip_routes: list[Route] = [Route(target)]

    while wip_routes:
        # CLEAN!
        best_routes_by_head = {}

        for rt in wip_routes:
            if best_routes_by_head.get(rt.head) is None:
                best_routes_by_head[rt.head] = rt
            else:
                if len(rt.visited) < len(best_routes_by_head[rt.head].visited):
                    best_routes_by_head[rt.head] = rt
        
        wip_routes = []

        for ro in best_routes_by_head.values():
            wip_routes.append(ro)

        new_routes = []
        dead_routes = []

        for r in wip_routes:
            neighbours = get_neighbours(height_map, r.head)

            c_height = height_map[r.head[0]][r.head[1]]

            valid_steps = []

            for n in neighbours:
                n_height = height_map[n[0]][n[1]]

                if n == start and val(c_height) - val(n_height) <= 1:
                    r.move(start)
                    return r

                if n in r.visited:
                    continue

                # only consider 1 down or same height
                if val(c_height) - val(n_height) <= 1:
                    valid_steps.append(n)

            # dead route
            if len(valid_steps) == 0:
                dead_routes.append(r)
            
            # continue same route
            if len(valid_steps) == 1:
                r.move(valid_steps[0])

            # branch
            if len(valid_steps) > 1:
                for step in valid_steps:
                    new_route = Route(r.head, r.visited)
                    new_route.move(step)
                    new_routes.append(new_route)
                    
                dead_routes.append(r)

        for dr in dead_routes:
            if dr in wip_routes:
                wip_routes.remove(dr)

        wip_routes += new_routes

    raise RuntimeError('No route found')


def part_1(input_path="input/day_12.txt"):
    height_map = get_height_map(input_path)

    start, target, _ = read_map(height_map)

    r = find_shortest_route(height_map, start, target)

    return len(r.visited) - 1


def part_2(input_path="input/day_12.txt"):
    height_map = get_height_map(input_path)

    start, target, pos_by_letter = read_map(height_map)

    starting_points = [start] + pos_by_letter['a']

    # the only 'b's are in a line at j = 1; so can only start from j = 0
    starting_points = list(filter(lambda p: p[1] == 0, starting_points))

    routes_lengths = []

    for sp in starting_points:
        route = find_shortest_route(height_map, sp, target)
        routes_lengths.append(len(route.visited) - 1)

    routes_lengths.sort()

    return routes_lengths[0]
