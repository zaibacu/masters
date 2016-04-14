import unittest
from rank.util.ngram import unpack


def compute_bow(words: list, dictionary: list, matcher: callable, limit: int):
    def word_inside_dict(_dict: list, word: str) -> bool:
        return any([True
                    for s in _dict
                    if matcher(s, word) <= limit
                    ])

    def match_dict_item(item: tuple, word: tuple) -> bool:
        return all([word_inside_dict(i, w)
                    for i, w in zip(item, word)])

    return [any([match_dict_item(d, w) for w in words])
            for d in dictionary]


def bow_string(bow):
    z = zip(range(0, len(bow)), bow)
    return " ".join(["f{0}:{1}".format(item[0], 1.0 if item[1] else 0.0) for item in z])


def vw_model(bow, rating=None):
    # [Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features
    if rating:
        return "{0} 1.0 |bow {1}".format(rating, bow_string(bow))
    else:
        return "|bow {0}".format(bow_string(bow))


def clean(x):
    return x.replace("\n", "").strip()


def load_dict(f):
    for l in f:
        yield set(map(lambda x: tuple(map(clean, x)), map(lambda x: set(x.split(",")), unpack(l))))


def load_raw(f):
    return map(lambda x: tuple(map(clean, x)), map(unpack, f.readlines()))


class BowTestCase(unittest.TestCase):
    @staticmethod
    def setUpClass():
        import logging
        logging.basicConfig(level=logging.DEBUG)

    def test_dict(self):
        from io import StringIO
        buff = StringIO("hello\nworld\n")
        result = list(load_dict(buff))
        expected = [{("hello", )}, {("world",)}]
        self.assertEqual(expected, result)

    def test_raw(self):
        from io import StringIO
        buff = StringIO("hello\nworld\n")
        result = list(load_raw(buff))
        expected = [("hello", ), ("world",)]
        self.assertEqual(expected, result)

    def test_basic_bow(self):
        from io import StringIO
        from rank.util import levenshtein
        d = StringIO("hello,hi\nworld\n")
        r = StringIO("hi\nthere\nfellow\n")
        _dict = list(load_dict(d))
        _raw = list(load_raw(r))
        result = compute_bow(_raw, _dict, levenshtein, 0)
        expected = [True, False]
        self.assertEqual(expected, result)

    def test_ngram_bow(self):
        from io import StringIO
        from rank.util import levenshtein
        from argparse import Namespace
        d = StringIO("hello,hi\nworld\n")
        r = StringIO("hi\nworld\n")

        """
        (hi,hello|world) vs (hi|world)
        """
        d_buff = StringIO()
        r_buff = StringIO()
        import ngram
        ngram.main(Namespace(n=2), d, d_buff)
        ngram.main(Namespace(n=2), r, r_buff)
        d_buff.seek(0)
        r_buff.seek(0)

        _dict = list(load_dict(d_buff))
        _raw = list(load_raw(r_buff))
        print("Dict: {0}".format(_dict))
        print("Text: {0}".format(_raw))
        result = compute_bow(_raw, _dict, levenshtein, 0)
        print(result)


def main(args, _in, _out):
    parts = args.matcher_fn.split(".")
    module = __import__(".".join(parts[:-1]), fromlist=[""])
    matcher = getattr(module, parts[-1])
    with open(args.f, "r") as f:
        _dict = list(load_dict(f))

    raw = list(load_raw(_in))

    bow = compute_bow(raw, _dict, matcher, args.max_dist)
    _out.write("{0}".format(vw_model(bow)))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", help="Dictionary file")
    parser.add_argument("--matcher_fn", help="class for matcher function (Default: rank.util.levenshtein)", default="rank.util.levenshtein")
    parser.add_argument("--max_dist", help="maximum distance to assume equal (Default: 2)", default=2)
    main(parser.parse_args(), sys.stdin, sys.stdout)
