from collections import Counter


def main(args, _in, _out):
    words = Counter(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), _in.read().split("\n"))))
    for word, count in words.most_common(args.l):
        _out.write("{0}\n".format(word))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", help="Take l most common items", type=int, default=1000)
    main(parser.parse_args(), sys.stdin, sys.stdout)
