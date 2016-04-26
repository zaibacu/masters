from collections import Counter


def main(args, _in, _out):
    words = Counter(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), _in.read().split("\n"))))
    if args.all:
        gen = map(lambda x: (x[1], x[0]), enumerate(words))
    else:
        gen = words.most_common(args.l)

    for word, count in gen:
        _out.write("{0}\n".format(word))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", help="Take l most common items", type=int, default=1000)
    parser.add_argument("--all", action="store_true", help="Just give all words?")
    main(parser.parse_args(), sys.stdin, sys.stdout)
