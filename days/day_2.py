def get_rounds(input_path):
    with open(input_path) as input:
        return list(
            map(
                lambda x: x.strip().split(' '),
                input.read().split('\n')
            )
        )

points_map = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

new_rules_results_map = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

rules_map = {
    'AX': 3,
    'BY': 3,
    'CZ': 3,

    'AZ': 0,
    'BX': 0,
    'CY': 0,

    'AY': 6,
    'BZ': 6,
    'CX': 6,
}

new_rules_map = {
    'AX': 3,
    'BX': 1,
    'CX': 2,

    'AY': 1,
    'BY': 2,
    'CY': 3,

    'AZ': 2,
    'BZ': 3,
    'CZ': 1,
}

def play_round(round, use_new_rules=False) -> 'tuple[int, int]':
    play = round[0] + round[1]

    if not use_new_rules:
        return rules_map[play], points_map[round[1]]
    else:
        return new_rules_results_map[round[1]], new_rules_map[play]


def part_1(input_path="input/day_2.txt"):
    rounds = get_rounds(input_path)

    score = 0

    for r in rounds:
        res, played = play_round(r)
        score = score + res + played

    return score

def part_2(input_path="input/day_2.txt"):
    rounds = get_rounds(input_path)

    score = 0

    for r in rounds:
        res, played = play_round(r, True)
        score = score + res + played

    return score
