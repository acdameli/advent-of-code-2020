from library import Solution as Base, SolutionPart


class Machine(object):
    def __init__(self, program:list):
        self.program = program
        self.pnt = 0
        self.acc = 0
        self.log = []
        self.full_log = []

    def run(self):
        while True:
            if self.pnt in self.log:
                raise Exception(f'Infinite loop detected {pnt}')

            if self.pnt >= len(self.program):
                # passed end of input so program terminates
                return self.acc

            self.step()

    def parse_cmd(self, line):
        parts = line.split(' ')
        return parts[0], int(parts[1])

    def step(self):
        op, val = self.parse_cmd(self.program[self.pnt])
        self.log.append(self.pnt)
        entry = {'pnt': self.pnt, 'op': op, 'val': val, 'acc': self.acc}
        self.full_log.append(entry)
        if op == 'acc':
            self.acc += val
        elif op == 'jmp':
            self.pnt += val
        if op != 'jmp':
            self.pnt += 1


class Part1(SolutionPart):
    def run(self, data:list):
        machine = Machine(data)
        try:
            machine.run()
        except Exception as e:
            return machine.acc


class Part2(SolutionPart):
    def run(self, data:list):
        swap = {'jmp': 'nop', 'nop': 'jmp'}
        for i in range(0, len(data)):
            rewrite = data.copy()
            if data[i][0:3] not in swap:
                continue

            rewrite[i] = f'{swap[data[i][0:3]]}{data[i][3:]}'
            try:
                m = Machine(rewrite)
                result = m.run()
                return result
            except Exception as e:
                pass

        raise Exception('No single rewrite line found')


class Solution(Base):
    parts = {1: Part1(), 2: Part2()}
