def main(args, _in, _out):
    pass

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser()
    parser.add_argument("-n", help="Minimal distance to match words", default=2, type=int)
    main(sys.stdin, sys.stdout)
