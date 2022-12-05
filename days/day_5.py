import re


def get_crates_and_procedure(input_path):
    with open(input_path) as f:
        crates_block, procedure_block = f.read().split('\n\n')

        stacks = []
        stack_lines = crates_block.split('\n')
        stack_lines.pop()

        crate_regex = re.compile(r'(   |\[[A-Z]\])(?: |$)')

        for sl in stack_lines:
            matches = crate_regex.findall(sl)

            for i, c in enumerate(matches):
                if len(stacks) <= i:
                    stacks.append([])
                
                if not c == '   ':
                    stacks[i].append(c[1])
        
        for stack in stacks:
            stack.reverse()
        
        #  ----

        moves = []

        procedure_regex = re.compile(r'move (\d+) from (\d+) to (\d+)$')

        for pl in procedure_block.split('\n'):
            match = procedure_regex.match(pl)

            if match:
                n, s, e = match.groups()
                moves.append([int(n), int(s), int(e)])

        return stacks, moves


def part_1(input_path="input/day_5.txt"):
    stacks, moves = get_crates_and_procedure(input_path)

    for n, s, e in moves:
        for _ in range(n):
            stacks[e-1].append(stacks[s-1].pop())

    result = ''

    for stack in stacks:
        result += stack[len(stack)-1]

    return result


def part_2(input_path="input/day_5.txt"):
    stacks, moves = get_crates_and_procedure(input_path)

    for n, s, e in moves:
        move = []

        for _ in range(n):
            move.append(stacks[s-1].pop())

        move.reverse()
        stacks[e-1] = stacks[e-1] + move

    result = ''

    for stack in stacks:
        result += stack[len(stack)-1]

    return result
