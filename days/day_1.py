def get_calories(input_path):
    with open(input_path) as input:
        return list(map(lambda x: x.strip(), input.readlines()))

def part_1(input_path="input/day_1.txt"):
    calories = get_calories(input_path)

    local_total = 0
    max_c = 0

    for c in calories:
        if c == "":
            max_c = max(max_c, local_total)
            local_total = 0
        else:
            local_total += int(c)
    
    # handle final elf
    max_c = max(max_c, local_total)

    return max_c

def part_2(input_path="input/day_1.txt"):
    calories = get_calories(input_path)

    inventories = []
    elf_total = 0

    for c in calories:
        if c == "":
            inventories.append(elf_total)
            elf_total = 0
        else:
            elf_total += int(c)

    # handle final elf
    inventories.append(elf_total)

    inventories.sort(reverse=True)

    return sum(inventories[0:3])
