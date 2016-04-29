import logging
import numpy as np
logger = logging.getLogger(__name__)


def parse_num(n: str) -> float:
    if len(n.strip()) == 0:
        return 0

    try:
        return float(n)
    except ValueError:
        logger.error("Fail to parse: {0}".format(n))
        return 0


def get_slices(lst, n):
    for i in range(0, len(lst), n):
        items = list(filter(lambda x: abs(x) > 0.1, lst[i:i+n]))
        s = np.array(items)
        fillers = list([s.mean() for i in range(0, n - s.size)])
        yield list(map(lambda x: 1 if x > 0 else 0, items + fillers))


def score(numbers: list, base: int) -> list:
    result = np.array([sum(s) for s in get_slices(numbers, base)])
    return result.mean()


def main(args, _in, _out):
    numbers = [parse_num(num) for num in _in.read().split("\n")]
    _out.write("{0}\n".format(score(numbers, args.base, args.limit)))

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--base", type=int, default=10, help="On what scale we want to base our score")
    main(parser.parse_args(), sys.stdin, sys.stdout)
