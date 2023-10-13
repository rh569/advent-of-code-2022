class Facing:
    def __init__(self, val):
        self.value = val
        self.label = 'R' if val == 0 else 'D' if val == 1 else 'L' if val == 2 else 'U'


class Transition:
    def __init__(self, from_facing: Facing, to_idx: int, to_facing: Facing) -> None:
        self.from_facing = from_facing
        self.to_idx = to_idx
        self.to_facing = to_facing


class Face:
    def __init__(self, face, r_trans: Transition, d_trans: Transition, l_trans: Transition, u_trans: Transition):
        self.face = face
        self.r_trans = r_trans
        self.d_trans = d_trans
        self.l_trans = l_trans
        self.u_trans = u_trans


def get_facings():
    facings = []

    for i in range(4):
        facings.append(Facing(i))
        
        if i > 0:
            facings[i - 1].right = facings[i]
    
    facings[-1].right = facings[0]

    for i, face in enumerate(facings):
        if i == 0:
            face.left = facings[-1]
        else:
            face.left = facings[i - 1]

    return facings


FACINGS = get_facings()


def from_label(label: str) -> Facing:
    return [f for f in FACINGS if f.label == label][0]


def get_input(input_path):
    with open(input_path) as input:
        map_block, raw_instructions = input.read().split('\n\n')

        board = []

        longest_line = 0
        for line in map_block.split('\n'):
            longest_line = max(longest_line, len(line))
            board.append(list(line))
        
        for line in board:
            if len(line) < longest_line:
                for _ in range(longest_line - len(line)):
                    line.append(' ')
        
        
        raw_instructions = list(raw_instructions)
        instructions = []
        num_str = ''

        for ri in raw_instructions:
            if not ri.isdigit():
                if len(num_str) > 0:
                    instructions.append(int(num_str))
                    num_str = ''
                instructions.append(ri)
            else:
                num_str += ri


        return (board, instructions)


def get_input_cube(input_path):
    with open(input_path) as input:
        map_block, raw_instructions = input.read().split('\n\n')

        map_lines = map_block.split('\n')
        longest_line = max([len(l) for l in map_lines])

        face_length = 50 if longest_line % 50 == 0 else 4

        faces = []
        faces_in_net_row = []

        for line in map_lines:
            face_parts_in_line = []
            first_char = -1

            for j, char in enumerate(line):
                if char == ' ':
                    continue

                # enables indexing of multiple faces on lines that start with empty space
                if first_char == -1:
                    first_char = j
                
                face_number_in_line = (j - first_char) // face_length

                if len(face_parts_in_line) < face_number_in_line + 1:
                    face_parts_in_line.append([])
                
                face_parts_in_line[face_number_in_line].append(char)
        
            for fp_idx, fp in enumerate(face_parts_in_line):
                if len(faces_in_net_row) < fp_idx + 1:
                    faces_in_net_row.append([])

                faces_in_net_row[fp_idx].append(fp)

            if len(faces_in_net_row[0]) == face_length:
                faces.extend(faces_in_net_row)
                faces_in_net_row = []
        
        raw_instructions = list(raw_instructions)
        instructions = []
        num_str = ''

        for ri in raw_instructions:
            if not ri.isdigit():
                if len(num_str) > 0:
                    instructions.append(int(num_str))
                    num_str = ''
                instructions.append(ri)
            else:
                num_str += ri
        
        if len(num_str) > 0:
            instructions.append(int(num_str))


        return (
            [map_face(face, face_index, face_length) for face_index, face in enumerate(faces)],
            instructions
        )


def map_face(face, face_index, face_length):
    # Example mappings
    if face_length == 4:
        if face_index == 0:
            r_trans = Transition(from_label('R'), 5, from_label('L'))
            d_trans = Transition(from_label('D'), 3, from_label('D'))
            l_trans = Transition(from_label('L'), 2, from_label('D'))
            u_trans = Transition(from_label('U'), 1, from_label('D'))
        elif face_index == 1:
            r_trans = Transition(from_label('R'), 2, from_label('R'))
            d_trans = Transition(from_label('D'), 4, from_label('U'))
            l_trans = Transition(from_label('L'), 5, from_label('U'))
            u_trans = Transition(from_label('U'), 0, from_label('D'))
        elif face_index == 2:
            r_trans = Transition(from_label('R'), 3, from_label('R'))
            d_trans = Transition(from_label('D'), 4, from_label('R'))
            l_trans = Transition(from_label('L'), 1, from_label('L'))
            u_trans = Transition(from_label('U'), 0, from_label('R'))
        elif face_index == 3:
            r_trans = Transition(from_label('R'), 5, from_label('D'))
            d_trans = Transition(from_label('D'), 4, from_label('D'))
            l_trans = Transition(from_label('L'), 2, from_label('L'))
            u_trans = Transition(from_label('U'), 0, from_label('U'))
        elif face_index == 4:
            r_trans = Transition(from_label('R'), 5, from_label('R'))
            d_trans = Transition(from_label('D'), 1, from_label('U'))
            l_trans = Transition(from_label('L'), 2, from_label('U'))
            u_trans = Transition(from_label('U'), 3, from_label('U'))
        else:
            r_trans = Transition(from_label('R'), 0, from_label('L'))
            d_trans = Transition(from_label('D'), 1, from_label('R'))
            l_trans = Transition(from_label('L'), 4, from_label('L'))
            u_trans = Transition(from_label('U'), 2, from_label('L'))

        return Face(face, r_trans, d_trans, l_trans, u_trans)
    # Real input mappings
    else:
        if face_index == 0:
            r_trans = Transition(from_label('R'), 1, from_label('R'))
            d_trans = Transition(from_label('D'), 2, from_label('D'))
            l_trans = Transition(from_label('L'), 3, from_label('R'))
            u_trans = Transition(from_label('U'), 5, from_label('R'))
        elif face_index == 1:
            r_trans = Transition(from_label('R'), 4, from_label('L'))
            d_trans = Transition(from_label('D'), 2, from_label('L'))
            l_trans = Transition(from_label('L'), 0, from_label('L'))
            u_trans = Transition(from_label('U'), 5, from_label('U'))
        elif face_index == 2:
            r_trans = Transition(from_label('R'), 1, from_label('U'))
            d_trans = Transition(from_label('D'), 4, from_label('D'))
            l_trans = Transition(from_label('L'), 3, from_label('D'))
            u_trans = Transition(from_label('U'), 0, from_label('U'))
        elif face_index == 3:
            r_trans = Transition(from_label('R'), 4, from_label('R'))
            d_trans = Transition(from_label('D'), 5, from_label('D'))
            l_trans = Transition(from_label('L'), 0, from_label('R'))
            u_trans = Transition(from_label('U'), 2, from_label('R'))
        elif face_index == 4:
            r_trans = Transition(from_label('R'), 1, from_label('L'))
            d_trans = Transition(from_label('D'), 5, from_label('L'))
            l_trans = Transition(from_label('L'), 3, from_label('L'))
            u_trans = Transition(from_label('U'), 2, from_label('U'))
        else:
            r_trans = Transition(from_label('R'), 4, from_label('U'))
            d_trans = Transition(from_label('D'), 1, from_label('D')) #!
            l_trans = Transition(from_label('L'), 0, from_label('D'))
            u_trans = Transition(from_label('U'), 3, from_label('U'))

        return Face(face, r_trans, d_trans, l_trans, u_trans)


def get_start(board):
    for col, tile in enumerate(board[0]):
        if tile == '.':
            return (0, col)
    
    raise RuntimeError(f'No start position in {board[0]}')


def get_tile_in_front(board, pos, facing):

    if facing.value == 0:
        raw_tile = (pos[0], pos[1] + 1)
    elif facing.value == 1:
        raw_tile = (pos[0] + 1, pos[1])
    elif facing.value == 2:
        raw_tile = (pos[0], pos[1] - 1)
    else:
        raw_tile = (pos[0] - 1, pos[1])

    # row out of bounds
    if raw_tile[0] < 0:
        bottom_most = len(board) - 1

        while board[bottom_most][raw_tile[1]] == ' ':
            bottom_most -= 1
        
        raw_tile = (bottom_most, raw_tile[1])
    if raw_tile[0] >= len(board):
        top_most = 0

        while board[top_most][raw_tile[1]] == ' ':
            top_most += 1
        
        raw_tile = (top_most, raw_tile[1])
    # col out of bounds
    if raw_tile[1] < 0:
        right_most = len(board[raw_tile[0]]) - 1

        while board[raw_tile[0]][right_most] == ' ':
            right_most -= 1
        
        raw_tile = (raw_tile[0], right_most)
    if raw_tile[1] >= len(board[raw_tile[0]]):
        right_most = 0

        while board[raw_tile[0]][right_most] == ' ':
            right_most += 1
        
        raw_tile = (raw_tile[0], right_most)

    if board[raw_tile[0]][raw_tile[1]] == ' ':
        while board[raw_tile[0]][raw_tile[1]] == ' ':
            if facing.value == 0:
                new_col = raw_tile[1] + 1 if raw_tile[1] + 1 < len(board[raw_tile[0]]) else 0
                raw_tile = (raw_tile[0], new_col)
            elif facing.value == 1:
                new_row = raw_tile[0] + 1 if raw_tile[0] + 1 < len(board) else 0
                raw_tile = (new_row, raw_tile[1])
            elif facing.value == 2:
                new_col = raw_tile[1] - 1 if raw_tile[1] > 0 else len(board[raw_tile[0]]) - 1
                raw_tile = (raw_tile[0], new_col)
            else:
                new_row = raw_tile[0] - 1 if raw_tile[0] > 0 else len(board) - 1
                raw_tile = (new_row, raw_tile[1])

    return (board[raw_tile[0]][raw_tile[1]], raw_tile)


def trace_path(board, instructions, pos, facing):
    for i in instructions:
        if i == 'R':
            facing = facing.right
        elif i == 'L':
            facing = facing.left
        else:
            for _ in range(i):
                in_front_tile, in_front_pos = get_tile_in_front(board, pos, facing)

                if in_front_tile == '.':
                    pos = in_front_pos

    return (pos, facing)


def get_next_face_pos(trans: Transition, face_pos: tuple[int, int], face_length: int) -> tuple[int, int]:
    i, j = face_pos

    if trans.from_facing.label == 'R':
        if trans.to_facing.label == 'R':
            return (i, 0)
        elif trans.to_facing.label == 'D':
            return (0, face_length - 1 - i)
        elif trans.to_facing.label == 'L':
            return (face_length - 1 - i, face_length - 1)
        else:
            return (face_length - 1, i)

    elif trans.from_facing.label == 'D':
        if trans.to_facing.label == 'R':
            return (face_length - 1 - j, 0)
        elif trans.to_facing.label == 'D':
            return (0, j)
        elif trans.to_facing.label == 'L':
            return (j, face_length - 1)
        else:
            return (face_length - 1, face_length - 1 - j)

    elif trans.from_facing.label == 'L':
        if trans.to_facing.label == 'R':
            return (face_length - 1 - i, 0)
        elif trans.to_facing.label == 'D':
            return (0, i)
        elif trans.to_facing.label == 'L':
            return (i, face_length - 1)
        else:
            return (face_length - 1, face_length - 1 - i)

    else:
        if trans.to_facing.label == 'R':
            return (j, 0)
        elif trans.to_facing.label == 'D':
            return (0, face_length - 1 - j)
        elif trans.to_facing.label == 'L':
            return (face_length - 1 - j, face_length - 1)
        else:
            return (face_length - 1, j)


def get_tile_in_front_cube(faces: list[Face], face_idx, face_pos, facing: Facing) -> tuple[str, int, tuple[int, int], Facing]:
    face = faces[face_idx]
    face_length = len(face.face)
    i, j = face_pos

    if facing.label == 'R':
        if j == face_length - 1:
            next_face_idx = face.r_trans.to_idx
            next_face_pos = get_next_face_pos(face.r_trans, face_pos, face_length)
            next_face = faces[next_face_idx]
            return (next_face.face[next_face_pos[0]][next_face_pos[1]], next_face_idx, next_face_pos, face.r_trans.to_facing)
        else:
            in_front_pos = (i, j+1)
            return (face.face[i][in_front_pos[1]], face_idx, in_front_pos, facing)

    elif facing.label == 'D':
        if i == face_length - 1:
            next_face_idx = face.d_trans.to_idx
            next_face_pos = get_next_face_pos(face.d_trans, face_pos, face_length)
            next_face = faces[next_face_idx]
            return (next_face.face[next_face_pos[0]][next_face_pos[1]], next_face_idx, next_face_pos, face.d_trans.to_facing)
        else:
            in_front_pos = (i+1, j)
            return (face.face[in_front_pos[0]][j], face_idx, in_front_pos, facing)
    
    elif facing.label == 'L':
        if j == 0:
            next_face_idx = face.l_trans.to_idx
            next_face_pos = get_next_face_pos(face.l_trans, face_pos, face_length)
            next_face = faces[next_face_idx]
            return (next_face.face[next_face_pos[0]][next_face_pos[1]], next_face_idx, next_face_pos, face.l_trans.to_facing)
        else:
            in_front_pos = (i, j-1)
            return (face.face[i][in_front_pos[1]], face_idx, in_front_pos, facing)
    
    else:
        if i == 0:
            next_face_idx = face.u_trans.to_idx
            next_face_pos = get_next_face_pos(face.u_trans, face_pos, face_length)
            next_face = faces[next_face_idx]
            return (next_face.face[next_face_pos[0]][next_face_pos[1]], next_face_idx, next_face_pos, face.u_trans.to_facing)
        else:
            in_front_pos = (i-1, j)
            return (face.face[in_front_pos[0]][j], face_idx, in_front_pos, facing)


def trace_path_cube(faces, instructions, face_idx, face_pos, facing):
    for i in instructions:
        if i == 'R':
            facing = facing.right
        elif i == 'L':
            facing = facing.left
        else:
            for _ in range(i):
                in_front_tile, in_front_face_idx, in_front_face_pos, in_front_facing = get_tile_in_front_cube(faces, face_idx, face_pos, facing)

                if in_front_tile == '.':
                    face_idx = in_front_face_idx
                    face_pos = in_front_face_pos
                    facing = in_front_facing

    return (face_idx, face_pos, facing)


def get_map_position(face_idx, face_pos, face_length):
    i, j = face_pos
    # Example
    if face_length == 4:
        if face_idx == 0:
            return (i, 2 * face_length + j)
        elif face_idx == 1:
            return (face_length + i, j)
        elif face_idx == 2:
            return (face_length + i, face_length + j)
        elif face_idx == 3:
            return (face_length + i, 2 * face_length + j)
        elif face_idx == 4:
            return (2 * face_length + i, 2 * face_length + j)
        else:
            return (2 * face_length + i, 3 * face_length + j)

    # Real input
    else:
        if face_idx == 0:
            return (i, face_length + j)
        elif face_idx == 1:
            return (i, 2 * face_length + j)
        elif face_idx == 2:
            return (face_length + i, face_length + j)
        elif face_idx == 3:
            return (2 * face_length + i, j)
        elif face_idx == 4:
            return (2 * face_length + i, face_length + j)
        else:
            return (3 * face_length + i, j)


def get_password(pos, facing):
    return (pos[0] + 1) * 1000 + (pos[1] + 1) * 4 + facing.value


def part_1(input_path="input/day_22.txt"):
    board, instructions = get_input(input_path)

    pos = get_start(board)
    facing = FACINGS[0]

    pos, facing = trace_path(board, instructions, pos, facing)

    return get_password(pos, facing)


def part_2(input_path="input/day_22.txt"):
    faces, instructions = get_input_cube(input_path)

    face_idx = 0
    face_pos = (0,0)
    facing = FACINGS[0]

    face_idx, face_pos, facing = trace_path_cube(faces, instructions, face_idx, face_pos, facing)
    
    map_pos = get_map_position(face_idx, face_pos, len(faces[0].face))

    # 84459 - too low
    return get_password(map_pos, facing)
