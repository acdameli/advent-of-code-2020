from sys import argv
from library import Solution as Base, SolutionPart


def find_2(lines, target=2020):
    d = {}
    for l in lines:
        v = int(l)
        if v in d.keys():
            return d[v], v
        else:
            d[target - v] = v
    raise Exception(f'No pair found sums to {target}')


def find_3(lines, target=2020):
    l = len(lines)
    for i in range(0, l - 2):
        for j in range(i + 1, l - 1):
            for k in range(j + 1, l):
                if lines[i] + lines[j] + lines[k] == target:
                    return lines[i], lines[j], lines[k]
    raise Exception(f'No triplet found sums to {target}')


def part_1(data: str):
    pair = find_2(data)
    return pair[0] * pair[1]


def part_2(data: str):
    triplet = find_3(data)
    return triplet[0] * triplet[1] * triplet[2]


class Part1(SolutionPart):
    def run(self, data:list):
        a, b = find_2([int(d) for d in data])
        return a * b

class Part2(SolutionPart):
    def run(self, data:list):
        a, b, c = find_3([int(d) for d in data])
        return a * b * c


class Solution(Base):
    parts = {1: Part1(), 2: Part2()}


if __name__ == '__main__':
    path = argv[1] if len(argv) > 1 else 'input.txt'
    data = [int(l) for l in open(path, 'r').read().splitlines()]
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

