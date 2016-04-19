import logging
from collections import namedtuple
ClusterPair = namedtuple("ClusterPair", ["left", "right", "distance"])

logger = logging.getLogger(__name__)


def distance(g1, g2, matcher):
    return min([
        matcher(i1, i2)
        for i1 in g1
        for i2 in g2
    ])


def main(args, _in, _out):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    import pandas as pd
    parts = args.matcher_fn.split(".")
    module = __import__(".".join(parts[:-1]), fromlist=[""])
    matcher = getattr(module, parts[-1])

    groups = map(lambda x: set(map(lambda y: y.strip(), x.split(","))), _in.read().split("\n"))

    df = pd.DataFrame([ClusterPair(g1, g2, distance(g1, g2, matcher))
                      for g1 in groups
                      for g2 in groups
                      if g1 != g2])

    logger.debug(df)

    """min(clusters, key=lambda x: x.distance)

    for group in groups:
        g = list(group)
        if len(group) > 0:
            _out.write("{0}\n".format(",".join(group)))"""


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--matcher_fn", help="class for matcher function (Default: rank.util.levenshtein)", default="rank.util.levenshtein")
    parser.add_argument("--max_dist", help="maximum distance to assume equal (Default: 2)", default=2)
    parser.add_argument("--debug", help="Show debug output", action="store_true")
    main(parser.parse_args(), sys.stdin, sys.stdout)
