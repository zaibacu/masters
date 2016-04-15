def purge(raw):
    return raw.replace("\n", " ")


def main(_in, _out):
    title = _in.read()
    from rank.collect.movie import get_comments
    for comment in get_comments(title.strip()):
        _out.write("?\t{0}\n".format(purge(comment)))

if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
