def get_monkeys(input_path):
    with open(input_path) as input:
        howlers = []
        waiters = []
        lines = [l.split(': ') for l in input.read().split('\n')]
        
        for name, job in lines:
            if job.isdigit():
                howlers.append([name, int(job)])
            else:
                left, op, right = job.split(' ')
                waiters.append([name, left, right, op])
        
        return (howlers, waiters)


def part_1(input_path="input/day_21.txt"):
    howlers, waiters = get_monkeys(input_path)

    while len(howlers) > 0:
        h_name, h_num = howlers.pop()

        if h_name == 'root':
            return h_num

        convert = []

        for w in waiters:
            if w[1] == h_name:
                w[1] = h_num
            if w[2] == h_name:
                w[2] = h_num
            
            if type(w[1]) is int and type(w[2]) is int:
                convert.append(w)
        
        for c in convert:
            if c[0] == 'root':
                print(c)
                
            howlers.append([c[0], int(eval(f'{c[1]}{c[3]}{c[2]}'))])
            waiters.remove(c)

    raise RuntimeError('root did not howl a number')


def part_2(input_path="input/day_21.txt"):
    howlers, waiters = get_monkeys(input_path)

    root = [w for w in waiters if w[0] == 'root'][0]
    humn = [h for h in howlers if h[0] == 'humn'][0]
    howlers.remove(humn)

    while len(howlers) > 0:
        h_name, h_num = howlers.pop()

        convert = []

        for w in waiters:
            if w[1] == h_name:
                w[1] = h_num
            if w[2] == h_name:
                w[2] = h_num
            
            if type(w[1]) is int and type(w[2]) is int:
                convert.append(w)
        
        for c in convert:
            howlers.append([c[0], int(eval(f'{c[1]}{c[3]}{c[2]}'))])
            waiters.remove(c)
    
    num = root[1] if type(root[2]) is str else root[2]
    next_name = root[1] if type(root[1]) is str else root[2]

    while next_name != 'humn':
        next_monkey = [w for w in waiters if w[0] == next_name][0]
        op = next_monkey[3]

        if type(next_monkey[1]) is str:
            # root = unknown 'op' 5
            next_num = next_monkey[2]
            next_name = next_monkey[1]

            if op == '/':
                num = num * next_num
            elif op == '-':
                num = num + next_num

        else:
            # root = 5 'op' unknown
            next_num = next_monkey[1]
            next_name = next_monkey[2]

            if op == '/':
                if num % next_num != 0:
                    print(f'not divisible: {next_num} / {num}')
                num = next_num // num
            elif op == '-':
                num = next_num - num

        if op == '+':
            num = num - next_num
        elif op == '*':
            if num % next_num != 0:
                print(f'not divisible: {num} / {next_num}')
            num = num // next_num

    # 8204572764413 - too high
    return num
