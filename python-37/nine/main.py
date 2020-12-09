from collections import deque

from library import Solution as Base, SolutionPart
from one.main import find_2, NotFoundException


class Part1(SolutionPart):
    def __init__(self, preamble_length:int):
        self.prelen = preamble_length

    def run(self, data:list):
        preamble = deque(data[0:self.prelen], self.prelen)
        for v in data[self.prelen:]:
            try:
                find_2(preamble, int(v))
            except NotFoundException:
                return v
            preamble.append(v)
        raise NotFoundException('No value found')


class Part2(Part1):
    def find_contiguous_from_start(self, lines, target):
        for i in range(1, len(lines)):
            s = sum(lines[0:i])
            if s == target:
                return lines[0:i]
            elif s > target:
                raise NotFoundException('No contiguous region from start')
        raise NotFoundException('No contiguous region from start')

    def find_contiguous_from_position(self, lines, target):
        for i in range(0, len(lines)):
            if lines[i] == target:
                continue  # skip over the one entry representing the target
            try:
                return self.find_contiguous_from_start(lines[i:], target)
            except NotFoundException:
                pass
        raise NotFoundException('No contiguous region found at all')

    def run(self, data:list):
        target = int(super(Part2, self).run(data))
        data = [int(i) for i in data]
        values = self.find_contiguous_from_position(data, target)
        values = sorted(values)
        return min(values) + max(values)


class Solution(Base):
    parts = {1: Part1(25), 2: Part2(25)}
