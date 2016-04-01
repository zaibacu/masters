def levenshtein(w1, w2):
    return 0


def main(args, _in, _out):
    pass

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser()
    parser.add_argument("-n", help="Minimal distance to match words", default=2, type=int)
    main(sys.stdin, sys.stdout)


import unittest


class DistanceSuite(unittest.TestCase):
    def test_compute_simple_diff(self):
        w1 = "Labas"
        w2 = "Laabas"
        self.assertEqual(1, levenshtein(w1, w2))


