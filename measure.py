def round_prediction(x, r):
    if x > r:
        return 1
    elif x < r:
        return -1
    else:
        return 0


def get_count(lst):
    return len(lst)


def test_model(labels, predictions, r):
    pairs = list(
                map(lambda x: {"target": x[0], "prediction": round_prediction(x[1], r)},
                      zip(labels, predictions))
                 )

    import pandas as pd
    import numpy as np
    stats = pd.DataFrame(pairs)

    results = stats.groupby(["target", "prediction"])

    def extract_group(key):
        if key in results.groups:
            data = results.get_group(key)
            return int(data.count()[0])
        else:
            return 0

    cross = {
        "TP": extract_group((1, 1,)),
        "TN": extract_group((-1, -1,)),
        "FP": extract_group((-1, 1,)),
        "FN": extract_group((1, -1,))
    }

    cross_df = pd.Series(cross)
    cross_df["P"] = cross_df["TP"] + cross_df["FN"]
    cross_df["N"] = cross_df["FP"] + cross_df["TN"]
    cross_df["recall"] = cross_df["TP"] / cross_df["P"]
    cross_df["precision"] = cross_df["TP"] / (cross_df["TP"] + cross_df["FP"])
    cross_df["accuracy"] = (cross_df["TP"] + cross_df["TN"])/ (cross_df["TP"] + cross_df["FP"] + cross_df["TN"] + cross_df["FN"])
    # (2 * cross_df["TP"]) / (2 * cross_df["TP"] + cross_df["FP"] + cross_df["FN"])
    cross_df["F1"] = 2 * (cross_df["precision"] * cross_df["recall"]) / (cross_df["precision"] + cross_df["recall"])
    cross_df["MCC"] = (cross_df["TP"] * cross_df["TN"] - cross_df["FP"] * cross_df["FN"]) / np.sqrt(
        (cross_df["TP"] + cross_df["FP"]) *
        (cross_df["TP"] + cross_df["FN"]) *
        (cross_df["TN"] + cross_df["FP"]) *
        (cross_df["TN"] + cross_df["FN"])
    )

    return cross_df


def load_labels():
    with open("data/test.comments", "r") as f:
        return list([float(line.split(" | ", 1)[0]) for line in f.readlines()])


def load_predictions(model):
    with open("pred.{0}.txt".format(model), "r") as f:
        return list(map(lambda x: float(x.strip()), f.readlines()))


def main(args):
    labels = load_labels()
    model = load_predictions(args.model)
    result = test_model(labels, model, args.r)
    print(result)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model", help="model name")
    parser.add_argument("-r", type=float, help="the limit", default=0)
    main(parser.parse_args())
