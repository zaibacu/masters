def main(args, _in, _out):
    pass

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", default=2, help="Number of n grams")
    main(parser.parse_args(), sys.stdin, sys.stdout)
