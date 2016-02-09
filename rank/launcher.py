def main(input, output):
    from rank.analysis.sentiment import get_mood
    from rank.analysis.word import get_words
    words = get_words(input.read())
    res = sum([get_mood(w) for w in words])
    output.write("{0}".format(res))

