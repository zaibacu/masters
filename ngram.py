from rank.util.ngram import make_ngram


def main(args, _in, _out):
    items = _in.read().split("\n")
    for item in make_ngram(items, args.n):
        _out.write("({0})\n".format("|".join(item)))

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", default=2, help="Number of n grams")
    main(parser.parse_args(), sys.stdin, sys.stdout)
