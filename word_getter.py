import re


escape_chars = [',', '.', '?', '!', '-', '/', '\r', '\n', ':', ';', '\xa0']


def purge(raw):
    return re.sub(r"[{0}]".format("".join(escape_chars)), r" ", raw)


def remove_whitespace(word):
    return re.sub(r"\s", r"", word)


def get_words(raw):
    return filter(lambda x: len(x) > 0, [remove_whitespace(w) for w in purge(raw).lower().split(" ")])


def main(_in, _out):
    for word in get_words(_in.read()):
        _out.write("{0}\n".format(word))


if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
