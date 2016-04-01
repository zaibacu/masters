from collections import Counter


def main(_in, _out):
    words = Counter(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), _in.read().split("\n"))))
    for word, count in words.items():
        _out.write("{0}\t{1}\n".format(word, count))


if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
