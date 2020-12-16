from library import SolutionPart
from time import sleep


class Rule(object):
    def __init__(self, line):
        self.label, self.groups = self._parse_line(line)

    def _parse_line(self, line) -> tuple:
        label = line.split(':')[0]
        values = line.strip().split(':')[1]
        groups = []
        for seg in values.split(' or '):
            groups.append(sorted([int(i) for i in seg.split('-')]))
        return label, groups

    def is_valid_value(self, value) -> bool:
        for group in self.groups:
            if group[0] <= value <= group[1]:
                return True
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        g_arr = ["-".join([str(_) for _ in g]) for g in self.groups]
        g_str = " or ".join(g_arr)
        return f'{self.label}: {g_str}'

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.label, self.groups) == (other.label, self.groups)

    def __ne__(self, other):
        return not(self == other)


class Ticket(object):
    def __init__(self, line):
        self.values = [int(i) for i in line.split(',')]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.values)


class Base(SolutionPart):
    def load(self, data:list) -> tuple:
        line, rules, tickets = 0, [], []
        while data[line]:
            rules.append(Rule(data[line]))
            line += 1
        line += 2
        tickets.append(Ticket(data[line]))
        line += 3
        while line < len(data):
            tickets.append(Ticket(data[line]))
            line += 1

        return rules, tickets

    def is_valid_ticket(self, ticket:Ticket, rules:list):
        for value in ticket.values:
            found = False
            for candidate in rules:
                if candidate.is_valid_value(value):
                    found = True
                    break
            if not found:
                return False, value
        return True, None

    def is_valid_rule_for_ticket(self, ticket:Ticket, rule:Rule) -> bool:
        for value in ticket.values:
            if rule.is_valid_valid(value):
                return True
        return False


class Part1(Base):
    def run(self, data:list) -> int:
        invalid = 0
        rules, tickets = self.load(data)
        for ticket in tickets:
            b, val = self.is_valid_ticket(ticket, rules)
            if not b:
                invalid += val
        return invalid


class Part2(Base):
    def valid_positions_for_rule(self, ticket:Ticket, rule:Rule) -> set:
        return {
            i
            for i, value in enumerate(ticket.values)
            if rule.is_valid_value(value)
        }

    def run(self, data:list) -> int:
        rules, tickets = self.load(data)
        valid_tickets = list(filter(lambda t: self.is_valid_ticket(t, rules)[0], tickets))
        print(valid_tickets)
        # determine labels
        #  iterate over every rule and find positions for valid tickets that apply to this rule
        #  using set arithmetic find the unique combination of rule => index that fits
        rule_positions = {}
        for r in rules:
            for t in valid_tickets:
                positions = self.valid_positions_for_rule(t, r)
                if not r in rule_positions:
                    rule_positions[r] = positions
                else:
                    rule_positions[r] = rule_positions[r].intersection(positions)

        # at this point r may apply to 1 or more ticket index
        # if 1: this must be the index for the rule
        # if more than 1, we must filter out all index options which MUST be the index for another rule
        while list(filter(lambda _set: len(_set) > 1, rule_positions.values())):
            for r, indices in rule_positions.items():
                if len(indices) != 1:
                    continue
                for r1, indices1 in rule_positions.items():
                    if r1 == r:
                        continue
                    rule_positions[r1] = rule_positions[r1].difference(rule_positions[r])
        print(rule_positions)

        # now we should have a single index for each rule, we have our ticket mapping rule:index for every rule, we can perform our final calculation
        # isolate my_tickets "Departure" label values
        # find product of isolated values
        my_ticket = tickets[0]
        prod = 1
        for r, indset in rule_positions.items():
            if r.label[0:len('departure')] == 'departure':
                prod *= my_ticket.values[list(indset)[0]]
        return prod
