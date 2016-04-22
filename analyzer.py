def parse_bow(line):
    import re
    feature_pattern = re.compile(r"((?P<feature_id>f\d+):(?P<feature_value>-?\d[.]\d+))")
    label_part, bow_part = line.split("|", 1)
    label, _ = label_part.split(" ", 1)
    features = [(f.group("feature_id"), f.group("feature_value"))
                for f in feature_pattern.finditer(bow_part)
                ]

    return label, features


def main(args, _in, _out):
    # format: -1 1.0 |bow f0:1.0 f1:1.0 f2:1.0 f3:1.0 f4:1.0 f5:1.0
    data = [parse_bow(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()

    main(parser.parse_args(), sys.stdin, sys.stdout)