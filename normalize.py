from stemmer import stemmer


def parse_line(line: str) -> tuple:
    from word_getter import get_words
    label, text = line.split(" | ", 1)
    return label, get_words(text)


def translate(word: str, mapping: list) -> str:
    from functools import reduce
    return reduce(lambda s, translation: s.replace(*translation), mapping, word)


def purge_accents(word: str) -> str:
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
    return translate(word, mapping)


def purge_common_errors(word: str) -> str:
    mapping = [
        ("w", "v"),
        ("iai", "ei"),
        ("k", "g"),
        ("p", "b"),
        ("i", "j")
    ]
    return translate(word, mapping)


def main(args, _in, _out):
    from rank.util.lemma import Lemmator
    lemma = Lemmator()
    st = stemmer.Stemmer()
    data = [parse_line(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    def get_lemma(word: str) -> str:
        l, t = lemma.get_lemma(word)
        return l

    def pipe(word: str, index: int, total: int) -> str:
        from functools import reduce
        rules = []
        if args.stem:
            rules.append(st.stem)

        if args.accents:
            rules.append(purge_accents)

        if args.common:
            rules.append(purge_common_errors)

        if args.lemma:
            rules.append(get_lemma)

        if args.position:
            def get_position():
                if index < total / 3:
                    return "S"
                elif index < total * 2 / 3:
                    return "M"
                else:
                    return "E"
            rules.append(lambda x: "{0}_{1}".format(x, get_position()))

        return reduce(lambda s, r: r(s), rules, word)

    for label, words in data:
        lst = list(words)
        cnt = len(lst)
        _out.write("{0} | {1}\n".format(label, " ".join([pipe(w, index, cnt) for index, w in enumerate(lst)])))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--stem", action="store_true", help="Use stemmer?")
    parser.add_argument("--accents", action="store_true", help="Remove accents?")
    parser.add_argument("--common", action="store_true", help="Remove common errors?")
    parser.add_argument("--lemma", action="store_true", help="Replace to lemma?")
    parser.add_argument("--position", action="store_true", help="Add position for word?")
    main(parser.parse_args(), sys.stdin, sys.stdout)
