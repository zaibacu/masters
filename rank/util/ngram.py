def make_bigram(g):
    return make_ngram(g, 2)


def make_trigram(g):
    return make_ngram(g, 3)


def make_ngram(g, n):
    return zip(*[g[i:] for i in range(n)])
