from abc import abstractmethod

from library import SolutionPart


FLOOR = '.'
EMPTY = 'L'
FULL = '#'


class Layout(object):
    def __init__(self, layout:list):
        self.layout = layout

    def _is(self, row, col, _type):
        return self.layout[row][col] == _type

    def step(self):
        new_layout = [r.copy() for r in self.layout]
        for r in range(0, len(self.layout)):
            for c in range(0, len(self.layout[r])):
                if self._is(r, c, FLOOR):
                    continue
                if self.can_fill(r, c):
                    new_layout[r][c] = FULL
                elif self.can_empty(r, c):
                    new_layout[r][c] = EMPTY
        self.layout = new_layout
        return self.layout

    def count(self, _type):
        return sum([
            int(char == _type)
            for col in self.layout
            for char in col
        ])

    def __str__(self):
        return self.to_str(self.layout)

    def to_str(self, l:list):
        s = ''
        for r in self.layout:
            s += ''.join(r) + '\n'
        return s

    @abstractmethod
    def can_fill(self, row, col):
        pass

    @abstractmethod
    def can_empty(self, row, col):
        pass


class AdjacentLayout(Layout):
    def count_adjacent(self, row, col):
        positions = [
            [r, c] for r, c in [
                [row - 1, col - 1],
                [row - 1, col],
                [row - 1, col + 1],
                [row, col - 1],
                [row, col + 1],
                [row + 1, col - 1],
                [row + 1, col],
                [row + 1, col + 1],
            ]
            if r >= 0 and c >= 0
            and r < len(self.layout) and c < len(self.layout[r])
        ]
        # positions to check are now set
        return sum([int(self._is(r, c, FULL)) for r, c in positions])

    def can_fill(self, row, col):
        return self._is(row, col, EMPTY) and self.count_adjacent(row, col) == 0

    def can_empty(self, row, col):
        return self._is(row, col, FULL) and self.count_adjacent(row, col) >= 4


class VisibleLayout(Layout):
    def count_visible(self, row, col):
        deltas = [
            [dy, dx]
            for dy in range(-1, 2)
            for dx in range(-1, 2)
            if not (dx == 0 and dy == 0)
        ]
        depth = 1
        count = 0
        while deltas:
            dy, dx = deltas[0]
            if not(0 <= row + dy < len(self.layout)):
                # keep inside limits
                deltas = deltas[1:]
                continue
            if not(0 <= col + dx < len(self.layout[row + dy])):
                # keep inside limits
                deltas = deltas[1:]
                continue

            if self.layout[row + dy][col + dx] != FLOOR:
                count += int(self.layout[row + dy][col + dx] == FULL)
                deltas = deltas[1:]
                continue
            deltas[0] = [
                deltas[0][0] + (deltas[0][0] // max(abs(deltas[0][0]), 1)),
                deltas[0][1] + (deltas[0][1] // max(abs(deltas[0][1]), 1))
            ]
        return count

    def can_fill(self, row, col):
        return self.count_visible(row, col) == 0

    def can_empty(self, row, col):
        return self.count_visible(row, col) >= 5


class Part1(SolutionPart):
    def run(self, data:list):
        data = [list(l) for l in data]
        layout = AdjacentLayout(data)
        last = None
        c = 0
        while last != layout.step():
            last = layout.layout
            c+=1
            if c >= 10000:
                print(f'{c} iterations')
                raise Exception('Something fucked up')
        return layout.count(FULL)

class Part2(SolutionPart):
    def run(self, data:list):
        data = [list(l) for l in data]
        layout = VisibleLayout(data)
        last = None
        c = 0
        while last != layout.step():
            last = layout.layout
            c+=1
            if c >= 10000:
                print(f'{c} iterations')
                raise Exception('Something fucked up')
        return layout.count(FULL)

