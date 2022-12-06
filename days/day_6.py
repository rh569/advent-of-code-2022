def _get_input(input_path):
    with open(input_path) as input:
        return input.read().strip()


def _find_unique_run(sequence: str, run_length: int):
    pos = 0

    frame = []

    for c in sequence:
        if len(frame) == run_length:
            frame = frame[1:]

        frame.append(c)
        pos += 1

        if len(set(frame)) == run_length:
            return pos

    raise RuntimeError('No unique run found')


def part_1(input_path="input/day_6.txt"):
    sequence = _get_input(input_path)

    return _find_unique_run(sequence, 4)


def part_2(input_path="input/day_6.txt"):
    sequence = _get_input(input_path)

    return _find_unique_run(sequence, 14)
