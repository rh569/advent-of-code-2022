class Num():
    def __init__(self, val, initial_pos, left):
        self.val = val
        self.initial_pos = initial_pos
        self.left = left
        self.right = None


def get_numbers(input_path) -> list[Num]:
    with open(input_path) as input:
        nums = []

        for i, ln in enumerate(input.read().split('\n')):
            left = None if i == 0 else nums[i-1]
            new_num = Num(val=int(ln), initial_pos=i, left=left)

            if left is not None:
                left.right = new_num

            nums.append(new_num)

        nums[0].left = nums[-1]
        nums[-1].right = nums[0]

        return nums


def get_x_away_from_n(n: Num, x: int) -> Num:
    current = n

    for _ in range(abs(x)):
        if x > 0:
            current = current.right

            if current == n:
                current = current.right
        else:
            current = current.left

            if current == n:
                current = current.left
    
    return current


def print_list(nums):
    current = [n for n in nums if n.val == 0][0]
    end = current.left

    s = '['

    while current != end:
        s += f'{current.val}, '
        current = current.right

    print(f'{s}{end.val}]')


def mix(nums: list[Num]) -> None:
    for n in nums:
        # print(f'Moving {n.val} in:')
        # print_list(nums)
        # no-op
        if n.val == 0:
            continue
        
        if n.val % (len(nums) - 1) == 0:
            # print(f'Perfect loop... ({n.val})')
            continue

        move_away_val = abs(n.val) % (len(nums) - 1)

        if n.val < 0:
            move_away_val *= -1

        # get number moving to
        target = get_x_away_from_n(n, move_away_val)

        # close gap
        n.left.right = n.right
        n.right.left = n.left

        if n.val > 0:
            n.left = target
            n.right = target.right
            target.right.left = n
            target.right = n
        else:
            n.left = target.left
            n.right = target
            target.left.right = n
            target.left = n
        
        # print_list(nums)


def find_coords(nums) -> int:
    current = [n for n in nums if n.val == 0][0]
    sum_nums = []

    for i in range(3000):

        if current.right is None:
            raise RuntimeError('Broken list')

        current = current.right

        if (i + 1) % 1000 == 0:
            sum_nums.append(current.val)
    
    return sum(sum_nums)


def part_1(input_path="input/day_20.txt"):
    nums = get_numbers(input_path)

    mix(nums)

    return find_coords(nums)


def part_2(input_path="input/day_20.txt"):
    nums = get_numbers(input_path)

    # apply decryption key
    for n in nums:
        n.val *= 811589153

    # mix 10 times
    for _ in range(10):
        mix(nums)

    return find_coords(nums)
