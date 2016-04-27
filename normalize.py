from stemmer import stemmer


def parse_line(line: str) -> tuple:
    from word_getter import get_words
    label, text = line.split(" | ", 1)
    return label, get_words(text)


def purge_accents(word: str) -> str:
    from functools import reduce
    mapping = [
        ("ą", "a"),
        ("č", "c"),
        ("ę", "e"),
        ("ė", "e"),
        ("į", "i"),
        ("š", "s"),
        ("ų", "u"),
        ("ū", "u"),
        ("ž", "z")
    ]
    return reduce(lambda s, translation: s.replace(*translation), mapping, word)


def main(args, _in, _out):
    st = stemmer.Stemmer()
    data = [parse_line(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    def pipe(word: str) -> str:
        if args.stem:
            word = st.stem(word)

        if args.accents:
            word = purge_accents(word)

        return word

    for label, words in data:
        _out.write("{0} | {1}\n".format(label, " ".join([pipe(w) for w in words])))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--stem", action="store_true", help="Use stemmer?")
    parser.add_argument("--accents", action="store_true", help="Remove accents?")
    main(parser.parse_args(), sys.stdin, sys.stdout)
