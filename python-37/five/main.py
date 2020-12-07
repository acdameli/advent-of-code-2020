from functools import reduce

from library import Solution as Base, SolutionPart


class PartBase(SolutionPart):
    @staticmethod
    def segment_to_int(segment:str):
        bin_map = {'F': 0, 'B': 1, 'L': 0, 'R': 1}
        return reduce(lambda a, c: bin_map[c] + (a * 2), segment, 0)

    def seat_id(self, code):
        return (self.segment_to_int(code[:-3]) * 8) + self.segment_to_int(code[-3:])


class Part1(PartBase):
    def run(self, data: list):
        return max([self.seat_id(code) for code in data])


class Part2(PartBase):
    def run(self, data: list):
        seats = sorted([self.seat_id(code) for code in data])
        for i in range(0, len(seats)-1):
            if seats[i] + 1 != seats[i + 1]:
                return seats[i] + 1


class Solution(Base):
    parts = {1: Part1(), 2: Part2()}
