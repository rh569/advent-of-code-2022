from typing import Callable


def get_monkeys(input_path):
    with open(input_path) as input:
        blocks = input.read().split('\n\n')

        monkeys = []

        for b in blocks:
            lines = b.split('\n')

            id = divisor = testPass = testFail = -1
            items = None
            op = None

            for l in lines:
                if l[:7] == 'Monkey ':
                    id = int(l[7:-1])
                elif l[:18] == '  Starting items: ':
                    items = list(map(int, l[18:].split(', ')))
                elif l[:19] == '  Operation: new = ':
                    op = parse_op(l[19:])
                elif l[:21] == '  Test: divisible by ':
                    divisor = int(l[21:])
                elif l[:29] == '    If true: throw to monkey ':
                    testPass = int(l[29:])
                elif l[:30] == '    If false: throw to monkey ':
                    testFail = int(l[30:])
            
            monkeys.append(
                Monkey(id, items, op, divisor, testPass, testFail)
            )

        return monkeys


def parse_op(op: str) -> Callable[[int], int]:
    parts = op.split(' ')

    if parts[2] == 'old':
        if parts[1] == '*':
            return lambda x: x * x
        elif parts[1] == '+':
            return lambda x: x + x
    else:
        if parts[1] == '*':
            return lambda x: x * int(parts[2])
        elif parts[1] == '+':
            return lambda x: x + int(parts[2])
    
    raise RuntimeError(f'Unhandled operation: {op}')


class Monkey():
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test_divisor: int
    test_pass_target: int
    test_fail_target: int
    inspect_count: int

    def __init__(self, id, items, op, div, test_pass, test_fail):
        self.id = id
        self.items = items
        self.operation = op
        self.test_divisor = div
        self.test_pass_target = test_pass
        self.test_fail_target = test_fail
        self.inspect_count = 0
    
    def __str__(self):
        return (f'Monkey {self.id}:\n  Items: {self.items}\n  Op: {self.operation}\n  Div: {self.test_divisor}\n' +
                f'  Pass: {self.test_pass_target}\n  Fail: {self.test_fail_target}')


def play_keep_away(monkeys: list[Monkey], n_rounds: int, very_worried = False) -> None:
    monkeys_by_id = dict([(m.id, m) for m in monkeys])

    # something, something primes; something something common multiple ???
    divisors_multiplied = 1
    divisors = [m.test_divisor for m in monkeys]

    for d in divisors:
        divisors_multiplied *= d

    for r in range(n_rounds):
        for m in monkeys:
            while m.items:
                item = m.items.pop(0)

                if very_worried:
                    item = item % divisors_multiplied

                item = m.operation(item)
                m.inspect_count += 1
                
                if not very_worried:
                    item = item // 3

                if item % m.test_divisor == 0:
                    monkeys_by_id[m.test_pass_target].items.append(item)
                else:
                    monkeys_by_id[m.test_fail_target].items.append(item)


def calculate_monkey_business(monkeys: list[Monkey]) -> int:
    inpection_counts = [m.inspect_count for m in monkeys]
    inpection_counts.sort(reverse=True)

    return inpection_counts[0] * inpection_counts[1]


def part_1(input_path="input/day_11.txt"):
    monkeys = get_monkeys(input_path)

    play_keep_away(monkeys, 20)

    return calculate_monkey_business(monkeys)


def part_2(input_path="input/day_11.txt"):
    monkeys = get_monkeys(input_path)

    play_keep_away(monkeys, 10000, very_worried=True)

    return calculate_monkey_business(monkeys)
