def compute_bow(words, dictionary, matcher, limit):
    return [any([True
                 for s in d
                 for w in words
                 if matcher(s, w) <= limit
                 ])

            for d in dictionary]


def bow_string(bow):
    z = zip(range(0, len(bow)), bow)
    return " ".join(["f{0}:{1}".format(item[0], 1.0 if item[1] else 0.0) for item in z])


def vw_model(rating, bow):
    # [Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features
    return "{0} 1.0 |bow {1}".format(rating, bow_string(bow))


def clean(x):
    return x.replace("\n", "").strip()


def main(args, _in, _out):
    parts = args.matcher_fn.split(".")
    module = __import__(".".join(parts[:-1]), fromlist=[""])
    matcher = getattr(module, parts[-1])
    _dict = []
    with open(args.f, "r") as f:
        for l in f:
            _dict.append(set(map(clean, l.split(","))))

    raw = list(map(clean, _in.readlines()))

    bow = compute_bow(raw, _dict, matcher, args.max_dist)
    _out.write("{0}".format(bow_string(bow)))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", help="Dictionary file")
    parser.add_argument("--matcher_fn", help="class for matcher function (Default: rank.util.levenshtein)", default="rank.util.levenshtein")
    parser.add_argument("--max_dist", help="maximum distance to assume equal (Default: 2)", default=2)
    main(parser.parse_args(), sys.stdin, sys.stdout)
