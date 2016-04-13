def make_bigram(g):
    return make_ngram(g, 2)


def make_trigram(g):
    return make_ngram(g, 3)


def make_ngram(g, n):
    return zip(*[g[i:] for i in range(n)])


def unpack(raw: str) -> list:
    import re
    patt = re.compile(r"(?P<item>.*)*")
    results = patt.findall(raw)
    if len(results) > 0:
        return results
    else:
        return raw
