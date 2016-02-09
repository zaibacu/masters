

def main(input, output):
    from rank.analysis.sentiment import get_mood
    from rank.analysis.word import get_words
    from rank.util.ngram import make_bigram
    words = get_words(input.read())
    res = sum([get_mood(w) for w in make_bigram(words)])
    output.write("{0}".format(res))

