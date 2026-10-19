import sys

from pl0.parser.parser import parse


def main():
    if len(sys.argv) < 2:
        raise ValueError("expected a source file as argument")

    source_file = sys.argv[1]

    with open(source_file, "r") as f:
        ast = parse(f.read())
        print(ast)


if __name__ == "__main__":
    main()
