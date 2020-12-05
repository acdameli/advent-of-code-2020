from sys import argv


def parse_line(line):
    parts = line.split(' ')
    return (
        int(parts[0].split('-')[0]),
        int(parts[0].split('-')[1]),
        parts[1][0],
        parts[2]
    )


def part_1(lines):
    count = 0
    for l in lines:
        try:
            _min, _max, char, pw = parse_line(l)
        except:
            continue
        count += int(_min <= pw.count(char) <= _max)
    return count


def part_2(lines):
    count = 0
    for l in lines:
        try:
            _min, _max, char, pw = parse_line(l)
        except:
            continue
        try:
            count += int(
                bool(pw[_min - 1] == char) != bool(pw[_max - 1] == char)
            )
        except Exception as e:
            print(_min, _max, char, pw)
            raise e
    return count

if __name__ == '__main__':
    path = argv[1] if len(argv) > 1 else 'input.txt'
    data = open(path, 'r').readlines()
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

