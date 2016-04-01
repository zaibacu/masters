from stemmer import stemmer


def main(_in, _out):
    st = stemmer.Stemmer()
    groups = map(lambda x: set(map(lambda y: y.strip(), x.split(","))), _in.read().split("\n"))
    for group in groups:
        g = list(group)
        for item in g:
            # Add stemmed version to the group for each group member
            group.add(st.stem(item))
        if len(group) > 0:
            _out.write("{0}\n".format(",".join(group)))


if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
