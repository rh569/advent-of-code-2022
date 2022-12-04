def get_id_pairs(input_path):
    with open(input_path) as input:
        id_pairs = []

        for l in input.read().split('\n'):
            parts = l.split(',')
            id_pair = []

            for p in parts:
                id_pair.append(list(map(lambda x: int(x), p.split('-'))))
        
            id_pairs.append(id_pair)
    
    return id_pairs


def part_1(input_path="input/day_4.txt"):
    id_pairs = get_id_pairs(input_path)
    count = 0

    for ids in id_pairs:
        if (ids[0][0] <= ids[1][0] and ids[0][1] >= ids[1][1] or
            ids[0][0] >= ids[1][0] and ids[0][1] <= ids[1][1]):
            count += 1

    return count


def part_2(input_path="input/day_4.txt"):
    id_pairs = get_id_pairs(input_path)
    count = 0

    for ids in id_pairs:
        if (ids[0][0] <= ids[1][0] and ids[0][1] >= ids[1][0] or
            ids[0][0] >= ids[1][0] and ids[0][0] <= ids[1][1]):
            count += 1

    return count
