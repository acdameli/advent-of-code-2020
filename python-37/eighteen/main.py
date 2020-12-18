from abc import abstractmethod

from library import SolutionPart


class Component(object):
    @abstractmethod
    def evaluate(self) -> int:
        pass


class Expression(Component):
    def __init__(self, line):
        self.line = line

    def evaluate(self) -> int:
        componentslist = []
        i = 0
        while i < len(self.line):
            c = self.line[i]
            if c in '0123456789':
                # build Literal
                exp = self.line[i]
                while True:
                    if i + 1 >= len(self.line) or self.line[i+1] not in '0123456789':
                        break
                    i += 1
                    exp += self.line[i]
                componentslist.append(Literal(exp))
            elif c in ('+', '*'):
                # push operation to stack maybe?
                componentslist.append(Operation(c))
            elif c == ' ':
                pass
            elif c == '(':
                # read to corresponding ')'
                opens = 1
                exp = ''
                while i + 1 < len(self.line):
                    i += 1
                    c = self.line[i]
                    if c == ')':
                        if opens == 1:
                            expression = Literal(str(Expression(exp).evaluate()))
                            break
                        else:
                            opens -= 1
                    elif c == '(':
                        opens += 1
                    exp += c
                print(f'exp: {exp}')
                componentslist.append(expression)
            else:
                raise Exception(f'Unexpected character in input: {c}')
            i += 1
        lhs = componentslist[0]
        componentslist = componentslist[1:]
        for component in componentslist:
            if isinstance(component, Operation):
                component.lhs = lhs
                lhs = component
            elif isinstance(component, Literal):
                lhs.rhs = component
        return lhs.evaluate()


class Literal(Component):
    def __init__(self, value:str):
        self.value = value

    def evaluate(self) -> int:
        return int(self)

    def __int__(self):
        return int(self.value)


class Operation(Component):
    def __init__(self, op):
        self.op = op
        self._lhs = self._rhs = None

    @property
    def lhs(self) -> Component:
        return self._lhs

    @lhs.setter
    def lhs(self, v:Component):
        self._lhs = v

    @property
    def rhs(self) -> Component:
        return self._rhs

    @rhs.setter
    def rhs(self, v:Component):
        self._rhs = v

    def evaluate(self) -> int:
        if None in (self.lhs, self.rhs):
            raise Exception(f'Incorrectly formatted Operation {self.op}({self.lhs}, {self.rhs})')
        return (
            self.lhs.evaluate() + self.rhs.evaluate()
            if '+' == self.op
            else self.lhs.evaluate() * self.rhs.evaluate()
        )


class Part1(SolutionPart):
    def run(self, data:list):
        return sum([Expression(l).evaluate() for l in data])


class Part2(SolutionPart):
    def run(self, data:list):
        pass
