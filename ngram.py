import unittest
from rank.util.ngram import make_ngram, unpack


def main(args, _in, _out):
    items = _in.read().split("\n")
    for item in make_ngram(items, args.n):
        _out.write("({0})\n".format("|".join(item)))


class NGramTestCase(unittest.TestCase):
    def test_pack(self):
        data = ["hello", "world", "it", "is", "a", "lovely", "day"]
        result = list(make_ngram(data, 2))
        expected = [
            ("hello", "world"),
            ("world", "it"),
            ("it", "is"),
            ("is", "a"),
            ("a", "lovely"),
            ("lovely", "day"),
        ]
        self.assertEqual(expected, result)

    def test_unpack(self):
        raw = "(hello|world)"
        result = unpack(raw)
        print(result)
        expected = ["hello", "world"]
        # self.assertEqual(expected, result)


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", default=2, help="Number of n grams")
    main(parser.parse_args(), sys.stdin, sys.stdout)
