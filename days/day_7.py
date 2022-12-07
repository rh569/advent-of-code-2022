from typing import Optional, Union


def _get_lines(input_path):
    with open(input_path) as input:
        return input.read().split('\n')


class Dir():
    _files: 'list[File]'
    _total_size: Optional[int]
    _full_path: Optional[str]

    name: str
    parent: 'Optional[Dir]'
    dirs: 'list[Dir]'
    
    def __init__(self, name: str, parent: 'Optional[Dir]'):
        self.name = name
        self.parent = parent
        self.dirs = []

        self._files = []
        self._total_size = None
        self._full_path = None

    def add_dir(self, dir: 'Dir'):
        if not dir in self.dirs:
            self.dirs.append(dir)
    
    def add_file(self, file: 'File'):
        if not file in self._files:
            self._files.append(file)

    def get_full_path(self) -> str:
        if self._full_path is not None:
            return self._full_path

        if self.parent is None:
            return self.name
        else:
            return f'{self.parent.get_full_path()}+{self.name}'
    
    def get_total_size(self) -> int:
        if self._total_size is not None:
            return self._total_size

        direct_size = sum(map(lambda f: f.size, self._files))
        indirect_size = sum(map(lambda d: d.get_total_size(), self.dirs))

        size = direct_size + indirect_size
        self._total_size = size
        return size


class File():
    _name: str
    _dir: Dir

    size: int
    
    def __init__(self, name: str, dir: Dir, size: int):
        self.name = name
        self.size = size

        self._dir = dir


def _build_filesystem(lines: 'list[str]') -> 'tuple[Dir, dict[str, Dir]]':
    assert lines[0] == '$ cd /'
    lines = lines[1:]

    # set up filesystem root and dir map
    root = Dir('/', None)
    dirs_by_full_path = {
        root.name: root
    }

    # create the tree
    current_dir: Dir = root

    for l in lines:
        if l == '$ ls':
            continue

        elif l.startswith('$ cd'):
            target = l.split(' ')[2]

            if target == '..':
                if current_dir.parent is not None:
                    current_dir = current_dir.parent
            else:
                for d in current_dir.dirs:
                    if d.name == target:
                        current_dir = d
                        break

        elif l.startswith('dir'):
            _, name = l.split(' ')
            dir = Dir(name, current_dir)
            current_dir.add_dir(dir)
            dirs_by_full_path[dir.get_full_path()] = dir

        else:
            size_str, name = l.split(' ')
            file = File(name, current_dir, int(size_str))
            current_dir.add_file(file)

    return (root, dirs_by_full_path)


def part_1(input_path="input/day_7.txt"):
    terminal_lines = _get_lines(input_path)

    _, all_dirs = _build_filesystem(terminal_lines)

    sizes = []

    for d in all_dirs.values():
        sizes.append(d.get_total_size())
    
    total_size = 0

    for s in sizes:
        if s <= 100000:
            total_size += s

    # 1072909 -> too low
    return total_size


def part_2(input_path="input/day_7.txt"):
    terminal_lines = _get_lines(input_path)

    fs_root, all_dirs = _build_filesystem(terminal_lines)

    max_size = 70000000
    required = 30000000

    root_size = fs_root.get_total_size()
    free = max_size - root_size
    delete_required = required - free

    sizes = []

    for d in all_dirs.values():
        sizes.append(d.get_total_size())
    
    smallest_matching_delete_required = None

    for s in sizes:
        if s >= delete_required:
            if smallest_matching_delete_required is None:
                smallest_matching_delete_required = s
            else:
                smallest_matching_delete_required = min(s, smallest_matching_delete_required)

    return smallest_matching_delete_required
