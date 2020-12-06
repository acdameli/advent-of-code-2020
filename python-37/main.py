from click import argument, Choice, command, Path, option
from library import SolutionEngine


@command()
@argument('day', type=int, nargs=1)
@option('-i', '--in-file', 'in_file', type=Path(), required=False)
@option('-p', '--part', type=int, default=None, required=False, multiple=True)
def main(day, in_file, part):
    part = list(part) if part else [1,2]
    engine = SolutionEngine(day)
    data = open(in_file, 'r').read().splitlines()
    solution = engine.solution_class(data)
    failed = False
    for p in part:
        try:
            print(f'Part {p}: {solution.run_part(p)}')
        except Exception as e:
            print(f'Part {p} failed: {str(e)}')
            failed = True
    return not failed


if __name__ == '__main__':
    exit(int(main()))

