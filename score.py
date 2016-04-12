import logging
logger = logging.getLogger(__name__)


def parse_num(n: str) -> float:
    if len(n.strip()) == 0:
        return 0

    try:
        return float(n)
    except ValueError:
        logger.error("Fail to parse: {0}".format(n))
        return 0


def score(numbers: list, base: int, limit: int) -> list:
    import pandas as pd
    import numpy as np
    df = pd.Series(numbers)
    dist = np.random.normal(0, 0.5, 1000)

    def find_percentile(x: float) -> float:
        quantiles = list(np.arange(1, 0, -0.01))
        for q in quantiles:
            curve = pd.Series(dist).quantile(q=q)
            if x >= curve:
                return q
        return 0

    def transform(x):
        return find_percentile(x) * 10

    data = map(transform, filter(lambda x: abs(0 - x) > limit, numbers))
    df = pd.Series(data)
    return [df.std(), df.mean(), df.median()]


def main(args, _in, _out):
    numbers = [parse_num(num) for num in _in.read().split("\n")]
    _out.write("{0}\n".format(score(numbers, args.base, args.limit)))

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--base", type=int, default=10, help="On what scale we want to base our score")
    parser.add_argument("--limit", type=float, default=0.1, help="Minimum delta from 0 to accept score")
    main(parser.parse_args(), sys.stdin, sys.stdout)
