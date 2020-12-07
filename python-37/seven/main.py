from library import Solution as Base, SolutionPart


class Bag(object):
    def __init__(self, description):
        self.description = description
        self.can_contain = set()
        self.counts = {}

    def holds(self, bag:'Bag'):
        return bag.description in self.counts or any([
            b.holds(bag) for b in self.can_contain
        ])

    def add_bag(self, bag:'Bag', count:int):
        self.can_contain.add(bag)
        self.counts[bag.description] = count
        return self

    def count_sub_bags(self):
        return sum([
            self.counts[b.description] + self.counts[b.description] * b.count_sub_bags()
            for b in self.can_contain
        ])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}({})'.format(
            self.description,
            ', '.join(
                [f'{self.counts[b.description]} x {b}' for b in self.can_contain]
            )
        )


class BasePart(SolutionPart):
    def build_graph(self, lines:list):
        graph = {}
        for l in lines:
            self.parse_line(l, graph)

        return graph

    def parse_line(self, line:str, graph:dict={}):
        components = line.split(' ')
        description = ' '.join(components[0:2])
        bag = graph.get(description, Bag(description))
        for position in range(4, len(components), 4):
            if components[position] == 'no':
                continue
            desc = ' '.join(components[position + 1:position + 3])
            sub_bag = graph.get(desc, Bag(desc))
            graph[sub_bag.description] = sub_bag
            count = int(components[position])
            bag.add_bag(sub_bag, count)
        graph[bag.description] = bag

    def count_top_contains(self, graph:dict, bag:Bag):
        count = 0
        for b in graph.values():
            if b.holds(bag):
                count += 1
        return count


class Part1(BasePart):
    def run(self, data:list):
        graph = self.build_graph(data)
        bag = graph.get('shiny gold')
        return self.count_top_contains(graph, bag)


class Part2(BasePart):
    def run(self, data:list):
        graph = self.build_graph(data)
        bag = graph.get('shiny gold')
        return bag.count_sub_bags()


class Solution(Base):
    parts = {1: Part1(), 2: Part2()}
