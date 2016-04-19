import logging
import unittest
from collections import namedtuple
ClusterPair = namedtuple("ClusterPair", ["left", "right", "distance"])

logger = logging.getLogger(__name__)


def distance(g1, g2, matcher):
    import numpy as np
    logger.debug("Got {0} and {1} to match".format(g1, g2))
    if isinstance(g1, set) and isinstance(g2, set):
        return min([
                    matcher(i1, i2)
                    for i1 in g1
                    for i2 in g2
                ])
    else:
        return np.nan


def clustering(groups, matcher):
    import pandas as pd
    import numpy as np

    df = pd.DataFrame([(g1, g2)
                      for g1 in groups
                      for g2 in groups
                      if g1 != g2], columns=["left", "right"])

    def df_dist(left, right):
        return list([distance(pair[0], pair[1], matcher) for pair in zip(left, right)])

    df = df.where(np.tril(np.ones(df.shape)).astype(np.bool))
    df["distance"] = df_dist(df["left"], df["right"])

    logger.debug(df)
    return df


class KNNTestCase(unittest.TestCase):
    @staticmethod
    def setUpClass():
        logging.basicConfig(level=logging.DEBUG)

    def test_grouping_step(self):
        from rank.util import levenshtein
        groups = [{"a", "b", "c"}, {"c", "d", "f"}]
        result = clustering(groups, levenshtein)
        logger.debug("Minimum: {0}".format(result.ix[result["distance"].idxmin()]))


def main(args, _in, _out):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    parts = args.matcher_fn.split(".")
    module = __import__(".".join(parts[:-1]), fromlist=[""])
    matcher = getattr(module, parts[-1])

    groups = map(lambda x: set(map(lambda y: y.strip(), x.split(","))), _in.read().split("\n"))

    clustering(groups, matcher)


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--matcher_fn", help="class for matcher function (Default: rank.util.levenshtein)", default="rank.util.levenshtein")
    parser.add_argument("--max_dist", help="maximum distance to assume equal (Default: 2)", default=2)
    parser.add_argument("--debug", help="Show debug output", action="store_true")
    main(parser.parse_args(), sys.stdin, sys.stdout)
