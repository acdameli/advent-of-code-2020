from library import SolutionPart, Solution as Base


class Game(object):
    def __init__(self, init):
        self.cache = {v: i for i, v in enumerate(init[:-1])}
        self.last = init[-1]
        self.len = len(init) - 1

    def step(self):
        last_index = self.cache.get(self.last)
        if last_index is None:
            value = 0
        else:
            value = self.len - last_index
        self.cache[self.last] = self.len
        self.last = value
        self.len+=1
        return self.len, value

    def __str__(self):
        return f'len {self.len} last {self.last} cache {self.cache}'


class Part1(SolutionPart):
    def run(self, data:list):
        for init in data:
            game = Game(init)
            for i in range(len(init), 2020):
                r, value = game.step()
            return value


class Part2(SolutionPart):
    def run(self, data:list):
        for init in data:
            game = Game(init)

            for i in range(len(init), 30000000):
                r, value = game.step()
            return value


class Solution(Base):
    parts = {1:Part1(),2:Part2()}
    def __init__(self, data:list):
        self.data = [[int(i) for i in l.split(',')] for l in data]
