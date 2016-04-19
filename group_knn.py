import logging
import unittest
from collections import namedtuple
ClusterPair = namedtuple("ClusterPair", ["left", "right", "distance"])

logger = logging.getLogger(__name__)


def distance(g1, g2, matcher):
    error_dist = 100
    logger.debug("Got {0} and {1} to match".format(g1, g2))
    if isinstance(g1, float) or isinstance(g2, float):
        return error_dist

    if len(g1) == 0 or len(g2) == 0:
        return error_dist  # big enough number

    return min([
                matcher(i1, i2)
                for i1 in g1
                for i2 in g2
            ])


def clustering(groups, matcher, max_dist):
    import pandas as pd
    import numpy as np

    logger.debug("Got groups: {0}".format(groups))

    df = pd.DataFrame([(g1, g2)
                      for g1 in groups
                      for g2 in groups
                      if g1 != g2], columns=["left", "right"])

    df = df.where(np.tril(np.ones(df.shape)).astype(np.bool))

    logger.debug("Working on df: {0}".format(df))

    def df_dist(left, right):
        return list([distance(pair[0], pair[1], matcher) for pair in zip(left, right)])

    while True:
        df["distance"] = df_dist(df["left"], df["right"])
        logger.debug(df)
        _min = df.ix[df["distance"].idxmin()]
        if _min["distance"] <= max_dist:
            for i in _min["right"]:
                _min["left"].add(i)
            _min["right"].clear()
        else:
            break

    return set(filter(lambda x: len(x) > 0, map(lambda x: tuple(sorted(x)), df["left"])))


class KNNTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_grouping_step(self):
        from rank.util import levenshtein
        groups = [{"a", "b", "c"}, {"c", "d", "f"}]
        result = clustering(groups, levenshtein, 2)
        expected = {("a", "b", "c", "d", "f")}
        self.assertSetEqual(expected, result)

    def test_different_sets(self):
        from rank.util import levenshtein
        groups = [{"labas", "vakaras"}, {"rytoj", "bus"}]
        result = clustering(groups, levenshtein, 2)
        expected = {("labas", "vakaras"), ("bus", "rytoj")}
        self.assertSetEqual(expected, result)


def main(args, _in, _out):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    parts = args.matcher_fn.split(".")
    module = __import__(".".join(parts[:-1]), fromlist=[""])
    matcher = getattr(module, parts[-1])

    groups = list(map(lambda x: set(map(lambda y: y.strip(), x.split(","))), _in.read().split("\n")))

    for result in clustering(groups, matcher, args.max_dist):
        _out.write("{0}\n".format(",".join(result)))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--matcher_fn", help="class for matcher function (Default: rank.util.levenshtein)", default="rank.util.levenshtein")
    parser.add_argument("--max_dist", help="maximum distance to assume equal (Default: 2)", default=2)
    parser.add_argument("--debug", help="Show debug output", action="store_true")
    main(parser.parse_args(), sys.stdin, sys.stdout)
