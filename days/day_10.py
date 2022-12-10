def get_ops(input_path):
    with open(input_path) as input:
        return list(map(lambda x: x.split(' '), input.read().split('\n')))


def draw(output, current_line, x):
    if len(current_line) == 40:
        output.append(current_line)
        current_line = []

    next_pixel = len(current_line)
    if x == next_pixel or x - 1 == next_pixel or x + 1 == next_pixel:
        current_line.append('#')
    else:
        current_line.append('.')
    
    return current_line


def print_output(o):
    for l in o:
        ol = ''
        for c in l:
            ol += c
        print(ol)


def part_1(input_path="input/day_10.txt"):
    ops = get_ops(input_path)

    cycle = 1
    x = 1
    op_index = 0
    current_op = None
    current_op_decrement = 0

    signal_every_20 = []

    for _ in range(220):
        if current_op is None and op_index < len(ops):
            current_op = ops[op_index]
            current_op_decrement = 1 if len(current_op) == 1 else 2

        # end of cycle
        cycle += 1
        current_op_decrement -= 1

        if current_op_decrement == 0 and current_op is not None:
            if len(current_op) == 2:
                x += int(current_op[1])

            current_op = None
            op_index += 1

        # track
        if (cycle + 20) % 40 == 0:
            signal_every_20.append(x * cycle)

    return sum(signal_every_20)


def part_2(input_path="input/day_10.txt"):
    ops = get_ops(input_path)

    cycle = 1
    x = 1
    op_index = 0
    current_op = None
    current_op_decrement = 0

    output = []
    current_line = []

    for _ in range(260):
        if current_op is None and op_index < len(ops):
            current_op = ops[op_index]
            current_op_decrement = 1 if len(current_op) == 1 else 2

        current_line = draw(output, current_line, x)

        # end of cycle
        cycle += 1
        current_op_decrement -= 1

        if current_op_decrement == 0 and current_op is not None:
            if len(current_op) == 2:
                x += int(current_op[1])

            current_op = None
            op_index += 1
    
    print_output(output)
    return 0
