from library import SolutionPart


NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'
FORWARD = 'F'
LEFT = 'L'
RIGHT = 'R'

# find current direction, multiply each element by amount
# then add to current position x/y to get new position
mult = {
    NORTH: [0, -1],
    EAST: [1, 0],
    SOUTH: [0, 1],
    WEST: [-1, 0],
}

# allow us to map between mathematical ops rotations and string const
# directions
directions = {
    NORTH: 0,
    EAST: 90,
    SOUTH: 180,
    WEST: 270,
}


def re_sign_amount(direction, amount):
    return [
        amount * mult[direction][0],
        amount * mult[direction][1]
    ]


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def move(self, x, y):
        return self.__class__(self.x + x, self.y + y)


class Direction(object):
    def __init__(self, direction):
        self.direction = direction

    def __str__(self):
        d = {NORTH:'^', EAST:'>', SOUTH:'v', WEST:'<'}
        return f'{d[self.direction]}'

    def __hash__(self):
        return self.direction

    def __eq__(self, other):
        return self.direction == other.direction

    def rotate_clockwise(self, amount):
        clockwise = [NORTH, EAST, SOUTH, WEST]
        return self._rotate(clockwise, amount)

    def rotate_counter(self, amount):
        counter = [WEST, SOUTH, EAST, NORTH]
        return self._rotate(counter, amount)

    def _rotate(self, dir_list, amount):
        ticks = (amount // 90)
        ind = dir_list.index(self.direction)
        return self.__class__(dir_list[(ind + ticks) % len(dirlist)])


class Pointing(object):
    def __init__(self, point:Point, direction:Direction):
        self.position = point
        self.direction = direction

    def __str__(self):
        return f'{self.position} {self.direction}'

    def move(self, direction, amount):
        m = mult[direction]
        point = self.point.move(amount * m[0], amount * m[1])
        return self.__class__(point, self.direction)

    def rotate(self, direction, amount):
        if direction == LEFT:
            amount = (360 - amount) % 360
        new_direction = self.direction.rotate(amount)
        return self.__class__(self.point, new_direction)


class Ship(object):
    def __init__(self, position:list=[0,0], direction=EAST):
        self.position = position
        self.direction = direction
        self.forward(0)  # seed log
        self.log = []

    def _record(self):
        cutesy = {
            NORTH: '^',
            SOUTH: 'v',
            EAST: '>',
            WEST: '<',
        }
        return {'position': self.position, 'direction': cutesy[self.direction]}

    def _log(self):
        self.log.append(self._record())

    def __sign(self, amount):
        return re_sign_amount(self.direction, amount)

    def forward(self, amount):
        p = self.position.copy()
        move = self.__sign(amount)
        p = [p[0] + move[0], p[1] + move[1]]
        self.position = p

    def rotate(self, direction, amount):
        rotation_mult = 1 if direction == RIGHT else -1
        degrees = (directions[self.direction] + (rotation_mult * amount)) % 360
        self.direction = list(directions.keys())[
            list(directions.values()).index(degrees)
        ]

    def strafe(self, direction, amount):
        d = self.direction
        self.direction = direction
        self.forward(amount)
        self.direction = d

    def move(self, instruction):
        c, amt = instruction[0], int(instruction[1:])
        if c == FORWARD:
            self.forward(amt)
        elif c in (LEFT, RIGHT):
            self.rotate(c, amt)
        else:
            self.strafe(c, amt)
        self._log()


class WaypointNavigator(object):
    def __init__(self, position=[0,0], waypoint=[0,0]):
        self.position = position
        self.waypoint = waypoint
        self.log = [{'ship': self.position, 'waypoint': self.waypoint}]

    def format_last(self):
        record = self.log[-1]
        return {'ship': self.position, 'waypoint': [
            str(abs(self.waypoint[0])) + ('W' if self.waypoint[0] < 0 else 'E'),
            str(abs(self.waypoint[1])) + ('N' if self.waypoint[1] < 0 else 'S')
        ]}

    def _record(self):
        return {'ship': self.position, 'waypoint': self.waypoint}

    def _log(self):
        self.log.append(self._record())

    def _rebuild_rotation(self, op, amt):
        return RIGHT, amt if op == RIGHT else (360 - amt) % 360

    def move_waypoint(self, op, amt):
        if op in (LEFT, RIGHT):
            def rot90(pos):
                return [pos[1]*-1, pos[0]]

            # modify amt so all L ops are R ops
            op, amt = self._rebuild_rotation(op, amt)
            for i in range(0, amt//90):
                self.waypoint = rot90(self.waypoint)
        else:
            # reposition waypoint, add amt to waypoint x/y
            movement = re_sign_amount(op, amt)
            self.waypoint[0] += movement[0]
            self.waypoint[1] += movement[1]

    def move(self, instruction):
        op, amt = instruction[0], int(instruction[1:])
        if op == FORWARD:
            dx = amt * self.waypoint[0]
            dy = amt * self.waypoint[1]
            self.position[0] += dx
            self.position[1] += dy
        else:
            self.move_waypoint(op, amt)
        self._log()


class Part1(SolutionPart):
    def run(self, data:list):
        ship = Ship()
        for l in data:
            ship.move(l)
        return abs(ship.position[0]) + abs(ship.position[1])


class Part2(SolutionPart):
    def run(self, data:list):
        ship = WaypointNavigator([0,0], [10,-1])
        for l in data:
            ship.move(l)
        return abs(ship.position[0]) + abs(ship.position[1])
