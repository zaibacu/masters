def purge(raw):
    return raw.replace("\n", " ")


def main(_in, _out):
    title = _in.read()
    from rank.collect.movie import get_comments
    for comment in map(purge, get_comments(title)):
        _out.write("{0}\n".format(comment))

if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
