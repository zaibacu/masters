def compute_bow(words, dictionary):
    return [any([s in words for s in d]) for d in dictionary]


def bow_string(bow):
    z = zip(range(0, len(bow)), bow)
    return " ".join(["f{0}:{1}".format(item[0], 1.0 if item[1] else 0.0) for item in z])


def vw_model(rating, bow):
    # [Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features
    return "{0} 1.0 |bow {1}".format(rating, bow_string(bow))


def clean(x):
    return x.replace("\n", "").strip()


def main(args, _in, _out):
    _dict = []
    with open(args.f, "r") as f:
        for l in f:
            _dict.append(set(map(clean, l.split(","))))

    raw = list(map(clean, _in.readlines()))

    bow = compute_bow(raw, _dict)
    _out.write("{0}".format(bow_string(bow)))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", help="Dictionary file")
    main(parser.parse_args(), sys.stdin, sys.stdout)
