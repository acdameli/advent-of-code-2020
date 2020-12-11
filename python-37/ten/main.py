from library import Solution as Base, SolutionPart

class Part1(SolutionPart):
    def run(self, data:list):
        last = 0
        diffs = []
        for i in data:
            if last + 3 < i:
                raise Exception(f'Could not find a next adapter last + 3 = {last + 3} < {i}')
            diffs.append(i - last)
            last = i
        diffs.append(3)
        ones = sum([i for i in diffs if i == 1])
        threes = sum([i for i in diffs if i == 3])//3
        print(diffs)
        print(f'{ones} ones, {threes} threes')
        return ones * threes


class Part2(SolutionPart):
    def naive(self, data:list):
        from collections import Counter
        data = [0] + data
        c = Counter({0:1})
        for x in data:
            c[x+1] += c[x]
            c[x+2] += c[x]
            c[x+3] += c[x]
        return c[max(data) + 3]

    def optimized(self, data:list):
        from functools import reduce
        places_to_go = []
        for i in range(0, len(data)):
            try:
                if i > 2 and data[i] <= data[i - 3] + 3:
                    places_to_go.append(3)
                elif i > 1 and data[i] <= data[i - 2] + 3:
                    places_to_go.append(2)
                elif i > 0 and data[i] <= data[i - 1] + 3:
                    places_to_go.append(1)

            except Exception as e:
                print(i, i-3)
                raise e

        return reduce(lambda x, y: x*y, places_to_go)

    def run(self, data:list):
        return self.naive(data)

class Solution(Base):
    parts = {1: Part1(), 2: Part2()}

    def __init__(self, data:list):
        self.data = sorted([int(i) for i in data])
