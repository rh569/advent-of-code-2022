def get_nums(input_path):
    with open(input_path) as input:
        return input.read().split("\n")


def decimalise(n: str) -> int:
    digits = list(n)
    digits.reverse()

    dec = 0

    for i, d in enumerate(digits):
        if d == "1" or d == "2":
            dec += 5**i * int(d)
        if d == "-":
            dec -= 5**i
        if d == "=":
            dec -= 5**i * 2

    return dec


def snafuise_quotient(quotient: int) -> str:
    assert quotient >= -2
    assert quotient <= 2

    map = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }

    return map[quotient]


def snafuise(dec_target: int) -> str:
    highest_required_position = 0
    cumulative_position_maximum = 2  # from  2 * 5^(0)
    position_maximums = [cumulative_position_maximum]

    # How many numerals are needed in bal-5?
    while dec_target > cumulative_position_maximum:
        highest_required_position += 1
        cumulative_position_maximum += 2 * (5**highest_required_position)
        position_maximums.append(cumulative_position_maximum)

    # Exit early for special case of all 2s
    if dec_target == cumulative_position_maximum:
        return "".join(["2" for _ in range(highest_required_position + 1)])

    # Start building string
    snafu_str = ""

    position = highest_required_position

    # Iterate back through the positions, appending the correct numeral
    while position >= 0:
        sign = -1 if dec_target < 0 else 1
        divisor = 5**position

        # Keep the divison of positive numerals to keep the quotient and remainders consistent
        # e.g, 10/3 => 3 r1 where -10/3 => -4 r2
        abs_quotient, abs_remainder = divmod(abs(dec_target), divisor)

        # Exit early for special cases of 'round' numbers
        if abs_remainder == 0:
            snafu_str += snafuise_quotient(sign * abs_quotient)
            return snafu_str + "".join(["0" for _ in range(position)])

        if abs_quotient == 0 and abs_remainder <= position_maximums[position - 1]:
            snafu_str += "0"
        elif abs_quotient == 0 and abs_remainder > position_maximums[position - 1]:
            snafu_str += snafuise_quotient(sign * 1)
            dec_target = dec_target - sign * divisor
        elif abs_quotient == 1 and abs_remainder <= position_maximums[position - 1]:
            snafu_str += snafuise_quotient(sign * 1)
            dec_target = sign * abs_remainder
        elif abs_quotient == 1 and abs_remainder > position_maximums[position - 1]:
            snafu_str += snafuise_quotient(sign * 2)
            dec_target = dec_target - sign * 2 * divisor
        elif abs_quotient == 2:
            snafu_str += snafuise_quotient(sign * 2)
            dec_target = sign * abs_remainder

        position -= 1

    return snafu_str


def part_1(input_path="input/day_25.txt"):
    nums = get_nums(input_path)

    dec_nums = [decimalise(n) for n in nums]
    dec_sum = sum(dec_nums)

    return snafuise(dec_sum)


def part_2(input_path="input/day_25.txt"):
    pass
