from collections import defaultdict
from copy import deepcopy
from functools import lru_cache

from library import SolutionPart


ACTIVE = '#'
INACTIVE = '.'


class Game(object):
    def __init__(self, init):
        self.board = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(lambda: INACTIVE)
            )
        )
        self.min_x = self.min_y = 0
        self.min_z = 0
        self.max_x = len(init)
        self.max_y = len(init[0])
        self.max_z = 1
        self.seed(init)

    def seed(self, init):
        z = 0
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                self.board[x][y][z] = init[x][y]

    def is_active(self, x, y, z):
        return self.board[x][y][z] == ACTIVE

    def neighbours(self, x, y, z):
        # working
        n = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if dx == dy == dz == 0:
                        continue
                    n.append((
                        x + dx,
                        y + dy,
                        z + dz,
                    ))
        return n

    def active_neighbours(self, x, y, z):
        c = 0
        for n in self.neighbours(x, y, z):
            c += 1 if self.is_active(*n) else 0
        return c

    @property
    def active(self):
        c = 0
        for x in self.board.keys():
            for y in self.board[x].keys():
                for z in self.board[x][y].keys():
                    c += 1 if self.board[x][y][z] == ACTIVE else 0
        return c

    def range(self, part):
        return range(
            min([int(i) for i in part.keys()]) - 1,
            max([int(i) for i in part.keys()]) + 1
        )

    def step(self):
        self.min_x -= 1
        self.min_y -= 1
        self.min_z -= 1
        self.max_x += 1
        self.max_y += 1
        self.max_z += 1
        new_board = deepcopy(self.board.copy())
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                for z in range(self.min_z, self.max_z):
                    active_neighbours = self.active_neighbours(x, y, z)
                    if self.board[x][y][z] == ACTIVE:
                        new_board[x][y][z] = ACTIVE if 2 <= active_neighbours <= 3 else INACTIVE
                    else:
                        new_board[x][y][z] = ACTIVE if 3 == active_neighbours else INACTIVE
        self.old_board = self.board
        self.board = new_board

    def print_board(self):
        for z in range(self.min_z, self.max_z):
            self.print_zslice(z)

    def print_zslice(self, z:int):
        print(f'z={z}')
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                print(f'{self.board[x][y][z]}',sep='',end='')
            print('')
        print('')


class Game2(Game):
    def __init__(self, init):
        self.board = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(
                    lambda: defaultdict(lambda: INACTIVE)
                )
            )
        )
        self.min_x = self.min_y = 0
        self.max_x = len(init)
        self.max_y = len(init[0])
        self.min_z = self.min_w = 0
        self.max_z = self.max_w = 1
        self.seed(init)

    def seed(self, init):
        z = 0
        w = 0
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                self.board[x][y][z][w] = init[x][y]

    def is_active(self, x, y, z, w):
        return self.board[x][y][z][w] == ACTIVE

    def neighbours(self, x, y, z, w):
        # working
        n = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    for dw in range(-1, 2):
                        if dx == dy == dz == dw == 0:
                            continue
                        n.append((
                            x + dx,
                            y + dy,
                            z + dz,
                            w + dw,
                        ))
        return n

    def active_neighbours(self, x, y, z, w):
        c = 0
        for n in self.neighbours(x, y, z, w):
            c += 1 if self.is_active(*n) else 0
        return c

    @property
    def active(self):
        c = 0
        for x in self.board.keys():
            for y in self.board[x].keys():
                for z in self.board[x][y].keys():
                    for w in self.board[x][y][z].keys():
                        c += 1 if self.board[x][y][z][w] == ACTIVE else 0
        return c

    def range(self, part):
        return range(
            min([int(i) for i in part.keys()]) - 1,
            max([int(i) for i in part.keys()]) + 1
        )

    def step(self):
        self.min_x -= 1
        self.min_y -= 1
        self.min_z -= 1
        self.min_w -= 1
        self.max_x += 1
        self.max_y += 1
        self.max_z += 1
        self.max_w += 1
        new_board = deepcopy(self.board.copy())
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                for z in range(self.min_z, self.max_z):
                    for w in range(self.min_w, self.max_w):
                        active_neighbours = self.active_neighbours(x, y, z, w)
                        if self.board[x][y][z][w] == ACTIVE:
                            new_board[x][y][z][w] = ACTIVE if 2 <= active_neighbours <= 3 else INACTIVE
                        else:
                            new_board[x][y][z][w] = ACTIVE if 3 == active_neighbours else INACTIVE
        self.old_board = self.board
        self.board = new_board

    def print_board(self):
        for z in range(self.min_z, self.max_z):
            for w in range(self.min_w, self.max_w):
                self.print_zslice(z, w)

    def print_zslice(self, z:int, w:int):
        print(f'z={z}, w={w}')
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                print(f'{self.board[x][y][z][w]}',sep='',end='')
            print('')
        print('')


class Part1(SolutionPart):
    def print_board(self, board):
        for x in sorted(board.keys()):
            for y in sorted(board[x].keys()):
                for z in sorted(board[x][y].keys()):
                    print(f'{x},{y},{z} = {board[x][y][z] == ACTIVE}')

    def run(self, data:list):
        game = Game(data)
        for i in range(0, 6):
            game.step()
        return game.active


class Part2(SolutionPart):
    def run(self, data:list):
        game = Game2(data)
        for i in range(0, 6):
            game.step()
        return game.active
