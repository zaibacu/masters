import logging
logger = logging.getLogger(__name__)


def parse_num(n: str) -> float:
    if len(n.strip()) == 0:
        return 0

    try:
        return float(n)
    except ValueError:
        logger.error("Fail to parse: {0}".format(n))
        return 0


def main(args, _in, _out):
    base = args.base
    numbers = [parse_num(num) for num in _in.read().split("\n")]
    _out.write("{0}\n".format(sum(numbers)))

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--base", type=int, default=10, help="On what scale we want to base our score")
    main(parser.parse_args(), sys.stdin, sys.stdout)
