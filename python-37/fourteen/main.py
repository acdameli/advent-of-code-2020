from library import SolutionPart


class Machine(object):
    def __init__(self):
        self.mem = {}
        self._mask = None

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, mask):
        self._mask = mask

    def __getitem__(self, item):
        return self.mem[item]

    def __setitem__(self, item, value):
        self.mem[item] = self.mask_value(value)

    def mask_value(self, value):
        bin_str = str(bin(value))[2:]
        bin_str = ('0' * (36 - len(bin_str))) + bin_str
        final = []
        for p in range(0, 36):
            if self.mask[p] != 'X':
                final.append(int(self.mask[p]))
            else:
                final.append(int(bin_str[p]))
        result = 0
        for i in final:
            result *= 2
            result += i
        return result

    def __str__(self):
        return str({
            'mask': self.mask,
            'mem': self.mem,
        })

    def __iter__(self):
        return iter(self.mem.values())

    def __next__(self):
        return next(self)


class Machine2(Machine):
    # totally stolen from the solutions megathread:
    # https://www.reddit.com/r/adventofcode/comments/kcr1ct/2020_day_14_solutions/gfvpe7a/
    @property
    def mask(self):
        # apparently can't reference @mask.setter from parent class's @property
        # mask
        return self._mask

    @mask.setter
    def mask(self, mask):
        if mask is None:
            self._x_mask = None
            self._1_mask = None
            return

        _x_mask = [False] * 36
        _1_mask = ['0'] * 36
        for i, c in enumerate(mask):
            if c == '1':
                _1_mask[i] = '1'
            elif c == 'X':
                _x_mask[i] = True

        self._1_mask = int(''.join(_1_mask), 2)
        self._x_mask = _x_mask

    def __set_bit(self, addr, index):
        return addr | (1<<index)

    def __clear_bit(self, addr, index):
        return addr & ~(1<<index)

    def __set(self, addr, value, index):
        if index == 36:
            self.mem[addr] = value
            return
        if self._x_mask[index]:
            self.__set(self.__set_bit(addr, 35-index), value, index+1)
            self.__set(self.__clear_bit(addr, 35-index), value, index+1)
            return
        while index < 36 and not self._x_mask[index]:
            index += 1
        self.__set(addr, value, index)

    def __setitem__(self, item, value):
        self.__set(item | self._1_mask, value, 0)


class Runner(object):
    def __init__(self, machine:Machine):
        self.machine = machine

    @staticmethod
    def parse_line(line):
        op, value = line.replace(' ', '').split('=')
        return op, int(value) if 'mask' != op else value

    def execute(self, line):
        op, value = self.parse_line(line)
        if op == 'mask':
            self.machine.mask = value
        else:
            index = int(op[4:-1])
            self.machine[index] = value


class Part1(SolutionPart):
    def run(self, data:list):
        runner = Runner(Machine())
        for l in data:
            runner.execute(l)
        print(runner.machine)
        return sum(runner.machine)

class Part2(SolutionPart):
    def run(self, data:list):
        runner = Runner(Machine2())
        for l in data:
            runner.execute(l)
        print(runner.machine)
        return sum(runner.machine)

