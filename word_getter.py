import re


escape_chars = [',', '.', '?', '!', '-', '/', '\r', '\n', ':', ';', '\xa0']


def purge(raw):
    return re.sub(r"[{0}]".format("".join(escape_chars)), r" ", raw)


def get_words(raw):
    return [w for w in raw.lower().split(" ") if len(w) > 0]


def main(_in, _out):
    for word in get_words(_in.read()):
        _out.write("{0}\n".format(word))


if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)