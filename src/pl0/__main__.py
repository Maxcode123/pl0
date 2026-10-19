import sys

from pl0.evaluator.errors import EvalError
from pl0.evaluator.evaluator import Evaluator
from pl0.parser.parser import parse


def main():
    if len(sys.argv) < 2:
        raise ValueError("expected a source file as argument")

    source_file = sys.argv[1]

    with open(source_file, "r") as f:
        ast = parse(f.read())

    try:
        Evaluator().run(ast)
    except EvalError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
