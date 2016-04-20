def main(args, _in, _out):
    ignore_list = []
    if args.i:
        with open(args.i, "r") as f:
            ignore_list = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), f.read().split("\n"))))

    words = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), _in.read().split("\n")))
    for word in words:
        if len(word) > args.l and word not in ignore_list:
            _out.write("{0}\n".format(word))

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser()
    parser.add_argument("-l", help="Minimal word length", default=3)
    parser.add_argument("-i", help="Ignore list")
    main(parser.parse_args(), sys.stdin, sys.stdout)
