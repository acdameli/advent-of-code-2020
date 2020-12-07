from library import Solution as Base, SolutionPart


class BasePart(SolutionPart):
    def validate_height(self, value):
        map = {
            'cm': [150, 193],
            'in': [59, 76],
        }
        h = value[0:-2]
        u = value[-2:]
        return u in map and map[u][0] <= int(h) <= map[u][1]

    @property
    @lru_cache()
    def validators(self):
        return {
            'byr': lambda v: 1920 <= int(v) <= 2002,
            'iyr': lambda v: 2010 <= int(v) <= 2020,
            'eyr': lambda v: 2020 <= int(v) <= 2030,
            'hgt': self.validate_height,
            'hcl': lambda v: v[0] == '#' and all([c in '0123456789abcdef' for c in v[1:len(v)]]),
            'ecl': lambda v: v in 'amb blu brn gry grn hzl oth'.split(' '),
            'pid': lambda v: len(v) == 9 and all([d in '0123456789' for d in v])
        }

    def run(self, data:list):
        for i in range(0, len(data)):
            if data[i] == '':
                if (
                    all([k in d for k in self.validators.keys()])
                    and all([
                        self.validate(f, v)
                        for f, v in d.items()
                        if f in self.validators.keys()
                    ])
                ):
                    count += 1
                d = {}
                continue
            for pair in data[i].split(' '):
                d[pair.split(':')[0]] = pair.split(':')[1]
        return count


class Part1(SolutionPart):
    def validate(self, field, value):
        return field in self.validators or field == 'cid'


class Part2(SolutionPart):
    def validate(self, field, value):
        return self.validators[field](value)



class Solution(Base):
    parts = {1: Part1(), 2: Part2()}
