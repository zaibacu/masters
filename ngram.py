def ngram(lst: list, n: int):
    return zip(*[lst[i:] for i in range(n)])


def main(args, _in, _out):
    items = _in.read().split("\n")
    for item in ngram(items, args.n):
        _out.write("({0})\n".format(item))

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", default=2, help="Number of n grams")
    main(parser.parse_args(), sys.stdin, sys.stdout)
