from library import SolutionPart


class Bus(object):
    def __init__(self, _id):
        self.id = int(_id) if _id != 'x' else 'x'

    def after(self, minutes):
        return self.id - (minutes % self.id)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self._id}'


class IndexedBus(Bus):
    def __init__(self, _id, index):
        self.index = index
        super(IndexedBus, self).__init__(_id)

    def __str__(self):
        return f'[{self.index}]{self.id}'

    def __int__(self):
        return int(self.id) if self.id != 'x' else None


class Part1(SolutionPart):
    def run(self, data:list):
        earliest = int(data[0])
        busses = {
            _id: Bus(int(_id)).after(earliest)
            for _id in data[1].split(',') if _id != 'x'
        }
        _min, _id = None, None
        for _i, t in busses.items():
            if not _min or _min > t:
                _min = t
                _id = _i

        return int(_id) * int(_min)


class Part2(SolutionPart):
    def run(self, data:list):
        schedule = data[1].split(',')
        busses = []
        for i in range(0, len(schedule)):
            if schedule[i] == 'x':
                continue
            busses.append(IndexedBus(schedule[i], i))
        bound = 1
        for b in busses:
            bound *= b.id if b.id != 'x' else 1
        solution = None
        for i in range(100000000000000, bound, int(b)):
            fail = False
            for b in busses:
                if (int(b) - (i % int(b))) % int(b) != b.index:
                    fail = True
                    break

            if not fail:
                return i
        return None
