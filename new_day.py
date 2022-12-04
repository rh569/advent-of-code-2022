import re
import sys


if __name__ != 'main':
    pass

n = -1

try:
    n = int(sys.argv[1])
except IndexError:
    print('Provide a day number')
    exit(1)

if n < 1:
    print('Provide a positive day number')
    exit(1)


# Create blank input files

with open(f'input/day_{n}.txt', 'x'):
    pass

with open(f'input/day_{n}_test.txt', 'x'):
    pass


# Copy template files

with open(f'templates/day.txt', 'r') as f:
    template = f.read()
    template = template.replace('{x}', str(n))
    
    with open(f'days/day_{n}.py', 'x') as new_f:
        new_f.write(template)

with open(f'templates/test_day.txt', 'r') as f:
    template = f.read()
    template = template.replace('{x}', str(n))
    
    with open(f'tests/test_day_{n}.py', 'x') as new_f:
        new_f.write(template)


# Add day to run.py

def add_import(match_obj: re.Match[str]) -> str:
    return f'{match_obj.group()}, day_{n}'


def add_day(match_obj: re.Match[str]) -> str:
    return f'{match_obj.group()}\n    day_{n},'


with open(f'run.py', 'r+') as f:
    run = f.read()
    run = re.sub(r'^from days import.+$', add_import, run, flags=re.M)

    pattern = r'^\s+' + f'day_{n-1},' + r'$'
    run = re.sub(pattern, add_day, run, flags=re.M)

    f.seek(0)
    f.write(run)


print('Done')
