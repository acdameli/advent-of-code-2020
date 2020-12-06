from sys import argv


def count_hits(lines, dy, dx):
    x, y = 0, 0
    hits = 0
    width = len(lines[0])
    while y < len(lines):
        hits += int(lines[y][x] == '#')
        x = (x + dx) % width
        y += dy
    return hits


def part_1(lines):
    return count_hits(lines, 1, 3)


def part_2(lines):
    result = 1
    tests = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    for dy, dx in tests:
        result *= count_hits(lines, dy, dx)
    return result

if __name__ == '__main__':
    path = argv[1] if len(argv) > 1 else 'input.txt'
    data = open(path, 'r').read().splitlines()
    try:
        part_1 = part_1(data)
    except Exception as e:
        part_1 = str(e)
    print(f'Part 1: {part_1}')
    try:
        part_2 = part_2(data)
    except Exception as e:
        part_2 = str(e)
    print(f'Part 2: {part_2}')

