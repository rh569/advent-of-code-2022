def get_cubes(input_path):
    with open(input_path) as input:
        return [list(map(int, coords.split(','))) for coords in input.read().split('\n')]


def get_all_unique_faces(cubes):
    faces = []

    for c in cubes:
        x, y, z = c

        cube_faces = [
            [[x,y,z],[x,y+1,z],[x+1,y+1,z],[x+1,y,z]], # front
            [[x,y,z],[x,y+1,z],[x,y+1,z+1],[x,y,z+1]], # left
            [[x,y,z+1],[x,y+1,z+1],[x+1,y+1,z+1],[x+1,y,z+1]], # back
            [[x+1,y,z],[x+1,y+1,z],[x+1,y+1,z+1],[x+1,y,z+1]], # right
            [[x,y+1,z],[x,y+1,z+1],[x+1,y+1,z+1],[x+1,y+1,z]], # top
            [[x,y,z],[x,y,z+1],[x+1,y,z+1],[x+1,y,z]], # bottom
        ]

        for cf in cube_faces:
            cf1, cf2, cf3, cf4 = cf
            face_to_remove = None

            for f in faces:
                if cf1 in f and cf2 in f and cf3 in f and cf4 in f:
                    face_to_remove = f

            if face_to_remove is not None:
                faces.remove(face_to_remove)
            else:
                faces.append(cf)
    
    return faces


def get_bounding_volume(cubes):
    x1, y1, z1 = cubes[0]
    bounding = [[x1, x1],[y1, y1],[z1, z1]]

    for c in cubes[1:]:
        x, y, z = c
        bounding[0][0] = min(bounding[0][0], x)
        bounding[0][1] = max(bounding[0][1], x)
        bounding[1][0] = min(bounding[1][0], y)
        bounding[1][1] = max(bounding[1][1], y)
        bounding[2][0] = min(bounding[2][0], z)
        bounding[2][1] = max(bounding[2][1], z)
    
    bounding[0][0] -= 1
    bounding[0][1] += 1
    bounding[1][0] -= 1
    bounding[1][1] += 1
    bounding[2][0] -= 1
    bounding[2][1] += 1

    return bounding


def in_bounding(pos, bounding_volume):
    return (
        pos[0] >= bounding_volume[0][0] and pos[0] <= bounding_volume[0][1]
        and
        pos[1] >= bounding_volume[1][0] and pos[1] <= bounding_volume[1][1]
        and
        pos[2] >= bounding_volume[2][0] and pos[2] <= bounding_volume[2][1]
    )


def add(p1, p2):
    return [p1[0]+p2[0], p1[1]+p2[1], p1[2]+p2[2]]


def find_enclosing_cubes(lava_cubes, bv):
    class Cube():
        def __init__(self, pos):
            self.pos = pos
            self.neighbours = list(map(lambda p: add(self.pos, p), [
                [1,0,0], [-1,0,0],
                [0,1,0], [0,-1,0],
                [0,0,1], [0,0,-1]
            ]))

    cubes_to_consider = [Cube([bv[0][0], bv[1][0], bv[2][0]])]
    considered_positions = []

    while len(cubes_to_consider) > 0:
        c = cubes_to_consider.pop()
        new_cubes = []

        for n in c.neighbours:
            if (in_bounding(n, bv) and
                n not in lava_cubes and
                n not in considered_positions and
                n not in [c.pos for c in cubes_to_consider]):
                new_cubes.append(Cube(n)) # todo, remove redundant face checks
        
        considered_positions.append(c.pos)
        cubes_to_consider = cubes_to_consider + new_cubes
    
    return considered_positions


def part_1(input_path="input/day_18.txt"):
    cubes = get_cubes(input_path)
    faces = get_all_unique_faces(cubes)

    return len(faces)


def part_2(input_path="input/day_18.txt"):
    cubes = get_cubes(input_path)
    bounding_volume = get_bounding_volume(cubes)
    enclosing_cubes = find_enclosing_cubes(cubes, bounding_volume)
    faces = get_all_unique_faces(enclosing_cubes)

    bounding_w = bounding_volume[0][1] - bounding_volume[0][0] + 1
    bounding_h = bounding_volume[1][1] - bounding_volume[1][0] + 1
    bounding_d = bounding_volume[2][1] - bounding_volume[2][0] + 1

    external_area = (
        2 * bounding_w * bounding_h +
        2 * bounding_w * bounding_d +
        2 * bounding_h * bounding_d
    )

    return len(faces) - external_area
