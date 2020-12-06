# Advent of Code 2020 - Python 3.7

## Usage

From within this directory: `docker-compose run worker python3 main.py {day} --in-file {path_to_input}`
1. runs day 1 with in-file found in subdirectory one/input.txt
2. optionally specify one or more --part (-p) with options with values 1 or 2 to target a specific part

```bash
# executes only part 2 of day 1
$ docker-compose run worker python3 main.py 1 --in-file one/input.txt -p 2
Creating python-37_worker_run ... done
Part 2: 276650720
```
