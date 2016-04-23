def parse_bow(line):
    import re
    feature_pattern = re.compile(r"((?P<feature_id>f\d+):(?P<feature_value>-?\d[.]\d+))")
    label_part, bow_part = line.split("|", 1)
    label, _ = label_part.split(" ", 1)
    features = [(f.group("feature_id"), float(f.group("feature_value")))
                for f in feature_pattern.finditer(bow_part)
                ]

    return {"label": int(label), **dict(features)}


def main(args, _in):
    import pandas as pd
    data = [parse_bow(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    df = pd.DataFrame(data)
    group = df.groupby("label")
    t = group.sum().transpose()
    t["diff"] = abs(t[-1] - t[1])/(t[-1] + t[1])
    columns = t[t["diff"] > args.n].index
    with open(args.m, "w") as f:
        f.write("\n".join(columns))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", type=float, help="limit to discard column", default=0.3)
    parser.add_argument("-m", help="Mask file")
    main(parser.parse_args(), sys.stdin)
