def make_bigram(g):
    return make_ngram(g, 2)


def make_trigram(g):
    return make_ngram(g, 3)


def make_ngram(g, n):
    if n > 1:
        return zip(*[g[i:] for i in range(n)])
    else:
        return g


def unpack(raw: str) -> tuple:
    import re
    patt = re.compile(r"((\w|[0-9,/!?])+)")
    results = tuple(map(lambda x: x[0], patt.findall(raw)))
    if len(results) > 0:
        return results
    else:
        return tuple(raw)
