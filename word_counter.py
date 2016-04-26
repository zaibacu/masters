from collections import Counter


def counter(words: list, limit: int, all: bool) -> list:
    cnt = Counter(words)
    if all:
        return map(lambda x: (x[1], x[0]), enumerate(cnt))
    else:
        return cnt.most_common(limit)


def main(args, _in, _out):
    gen = counter(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), _in.read().split("\n"))), args.l, args.all)

    for word, count in gen:
        _out.write("{0}\n".format(word))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", help="Take l most common items", type=int, default=1000)
    parser.add_argument("--all", action="store_true", help="Just give all words?")
    main(parser.parse_args(), sys.stdin, sys.stdout)
