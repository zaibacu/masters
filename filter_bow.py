def main(args, _in, _out):
    import pandas as pd
    from rank.util.feature import parse_bow, vw_model
    with open(args.m, "r") as f:
        mask = list(map(lambda x: x.strip(), f.read().split("\n")))

    data = [parse_bow(line)
            for line in map(lambda x: x.strip(), _in.read().split("\n"))
            if len(line) > 0
            ]

    df = pd.DataFrame(data)
    filtered = df[mask]
    for label, line in zip(df["label"], filtered.values):
        _out.write("{0}\n".format(vw_model(" ".join(
            map(lambda x: "{0}:{1}".format(*x), zip(filtered.columns, line))), label)
        ))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-m", help="Mask file")
    main(parser.parse_args(), sys.stdin, sys.stdout)
