def get_compartmentalised_rucksacks(input_path) -> 'list[tuple[str, str]]':
    with open(input_path) as input:
        return list(
            map(
                lambda x: (x[:len(x)//2], x[len(x)//2:]),
                input.read().split('\n')
            )
        )


def get_rucksacks(input_path) -> 'list[str]':
    with open(input_path) as input:
        return list(input.read().split('\n'))


def get_priority(c: str) -> int:
    assert len(c) == 1

    lower_offset = 96
    upper_offset = 38

    code = ord(c)

    return code -  lower_offset if code > 90 else code - upper_offset


def get_double_packed_type(pack: 'tuple[str, str]') -> str:
    # TODO: improve
    for c in pack[0]:
        if c in pack[1]:
            return c

    raise


def get_all_priorities(rucksacks: 'list[tuple[str, str]]') -> 'tuple[list[int], int]':
    priorities = []
    sum = 0

    for r in rucksacks:
        p = get_priority(get_double_packed_type(r))
        priorities.append(p)
        sum += p
    
    return priorities, sum


def split_into_groups(rucksacks):
    assert len(rucksacks) % 3 == 0

    groups = []
    new_group = []

    for r in rucksacks:
        new_group.append(r)
        
        if len(new_group) == 3:
            groups.append(new_group)
            new_group = []
        
    return groups


def get_group_badge(group) -> str:

    # TODO: definitely improve ...
    for i in group[0]:
        for j in group[1]:
            for k in group[2]:
                if i == j and j ==k:
                    return i
    
    raise


def part_1(input_path="input/day_3.txt"):
    rucksacks = get_compartmentalised_rucksacks(input_path)

    _, sum = get_all_priorities(rucksacks)

    return sum


def part_2(input_path="input/day_3.txt"):
    rucksacks = get_rucksacks(input_path)

    groups = split_into_groups(rucksacks)

    sum = 0

    for g in groups:
        p = get_priority(get_group_badge(g))
        sum += p

    return sum
