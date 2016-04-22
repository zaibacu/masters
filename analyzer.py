def parse_bow(line):
    import re
    feature_pattern = re.compile(r"((?P<feature_id>f\d+):(?P<feature_value>-?\d[.]\d+))")
    label_part, bow_part = line.split("|", 1)
    label, _ = label_part.split(" ", 1)
    features = [(f.group("feature_id"), float(f.group("feature_value")))
                for f in feature_pattern.finditer(bow_part)
                ]

    return {"label": int(label), **dict(features)}


def main(args, _in, _out):
    import pandas as pd
    # format: -1 1.0 |bow f0:1.0 f1:1.0 f2:1.0 f3:1.0 f4:1.0 f5:1.0
    data = [parse_bow(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    df = pd.DataFramed(data)
    group = df.groupby("label")
    t = group.sum().transpose()
    t["diff"] = abs(t[-1] - t[1])/(t[-1] + t[1])
    columns = t[t["diff"] > 0.3]  # Over 30% of difference
    optimized = df[columns]


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()

    main(parser.parse_args(), sys.stdin, sys.stdout)
