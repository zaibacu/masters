from Levenshtein import distance
import logging
logger = logging.getLogger(__name__)


def levenshtein(w1, w2):
    return distance(w1, w2)


def main(args, _in, _out):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    groups = list(map(lambda x: set(map(lambda y: y.strip(), x.split(","))), _in.read().split("\n")))
    changes_applied = True

    def needs_merge(g1, g2):
        return any([
            True
            for w1 in g1
            for w2 in g2
            if levenshtein(w1, w2) <= args.n
        ])

    def merge(g1, g2):
        return g1 | g2

    while changes_applied:
        changes_applied = False
        pairs = [
            (group1, group2,)
            for group1 in groups
            for group2 in groups
            if group1 != group2
        ]

        for pair in pairs:
            g1, g2 = pair
            if needs_merge(g1, g2):
                changes_applied = True
                g3 = merge(g1, g2)
                logger.debug("Removing {0} and {1}".format(g1, g2))

                groups.remove(g1)
                groups.remove(g2)
                logger.debug("Current groups: {0}".format(groups))
                logger.debug("Adding {0}".format(g3))
                groups.append(g3)
                break  # Cancel loop because of changes being done

    for group in groups:
        if len(group) > 0:
            _out.write("{0}\n".format(",".join(group)))


if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser()
    parser.add_argument("-n", help="Minimal distance to match words", default=2, type=int)
    parser.add_argument("--debug", help="Show debug output", action="store_true")
    main(parser.parse_args(), sys.stdin, sys.stdout)


import unittest


class DistanceSuite(unittest.TestCase):
    def test_compute_simple_diff(self):
        w1 = "Labas"
        w2 = "Laaabas"
        self.assertEqual(1, levenshtein(w1, w2))


