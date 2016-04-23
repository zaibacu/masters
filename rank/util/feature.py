def parse_bow(line):
    import re
    feature_pattern = re.compile(r"((?P<feature_id>f\d+):(?P<feature_value>-?\d[.]\d+))")
    label_part, bow_part = line.split("|", 1)
    label, _ = label_part.split(" ", 1)
    features = [(f.group("feature_id"), float(f.group("feature_value")))
                for f in feature_pattern.finditer(bow_part)
                ]

    return {"label": int(label), **dict(features)}


def vw_model(bow_string, rating=None):
    # [Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features
    if rating and rating != "?":
        return "{0} 1.0 |bow {1}".format(rating, bow_string)
    else:
        return "|bow {0}".format(bow_string)
