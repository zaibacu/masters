from Levenshtein import distance


def levenshtein(w1: tuple, w2: tuple) -> int:
    return min([
        distance(d1, d2)
        for d1, d2 in zip(w1, w2)
    ])
