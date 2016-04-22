def main(args, _in, _out):
    pass

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()

    main(parser.parse_args(), sys.stdin, sys.stdout)