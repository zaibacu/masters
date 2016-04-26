from stemmer import stemmer


def parse_line(line: str) -> tuple:
    from word_getter import get_words
    label, text = line.split(" | ", 1)
    return label, get_words(text)


def main(args, _in, _out):
    st = stemmer.Stemmer()
    data = [parse_line(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    for label, words in data:
        _out.write("{0} | {1}\n".format(label, " ".join([st.stem(w) for w in words])))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    main(parser.parse_args(), sys.stdin, sys.stdout)
