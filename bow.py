def compute_bow(words, dictionary):
    return [any([s in words for s in d]) for d in dictionary]


def bow_string(bow):
    z = zip(range(0, len(bow)), bow)
    return " ".join(["f{0}:{1}".format(item[0], 1.0 if item[1] else 0.0) for item in z])


def vw_model(rating, bow):
    # [Label] [Importance] [Base] [Tag]|Namespace Features |Namespace Features
    return "{0} 1.0 |bow {1}".format(rating, bow_string(bow))

