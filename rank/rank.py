def main(input, output):
    from rank.analysis.sentiment import get_mood
    input.read()
    output.write("0")

if __name__ == "__main__":
    import sys
    main(sys.stdin, sys.stdout)
