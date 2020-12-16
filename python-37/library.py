from abc import ABC, abstractmethod
from functools import lru_cache
from importlib import import_module


class Solution(ABC):
    def __init__(self, data:list):
        self.data = data

    @property
    @abstractmethod
    def parts(self):
        pass

    def run_part(self, num):
        return self.parts[num].run(self.data)


class SolutionPart(ABC):
    @abstractmethod
    def run(self, data:list):
        pass


class SolutionEngine(object):
    days = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
        7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
        13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
        17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty',
        21: 'twentyone', 22: 'twentytwo', 23: 'twentythree', 24: 'twentyfour',
        25: 'twentyfive'
    }
    def __init__(self, day):
        self.day = day

    def day_to_str(self, day):
        return self.days[day]

    @property
    @lru_cache()
    def solution_class(self):
        module = import_module(f'{self.day_to_str(self.day)}.main')
        try:
            return module.Solution
        except AttributeError:
            class DefaultSolution(Solution):
                parts = {1: module.Part1(), 2: module.Part2()}
            return DefaultSolution

