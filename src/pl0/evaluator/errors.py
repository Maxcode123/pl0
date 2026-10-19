class EvalError(Exception):
    """
    Base class of the errors raised while evaluating a program.
    """


class UndefinedNameError(EvalError):
    def __init__(self, name: str) -> None:
        super().__init__(f"undefined name {name!r}")
        self.name = name


class DuplicateNameError(EvalError):
    def __init__(self, name: str) -> None:
        super().__init__(f"name {name!r} is already declared in this block")
        self.name = name


class NameKindError(EvalError):
    """
    A name is used as something it isn't, e.g. assigning to a constant or
    calling a variable.
    """

    def __init__(self, name: str, kind: str, expected: str) -> None:
        super().__init__(f"{name!r} is a {kind}, expected a {expected}")
        self.name = name
        self.kind = kind
        self.expected = expected


class DivisionByZeroError(EvalError):
    def __init__(self) -> None:
        super().__init__("division by zero")


class InvalidInputError(EvalError):
    def __init__(self, text: str | None) -> None:
        if text is None:
            message = "expected an integer, reached the end of the input"
        else:
            message = f"expected an integer, read {text!r}"

        super().__init__(message)
        self.text = text


class RecursionDepthError(EvalError):
    def __init__(self) -> None:
        super().__init__("maximum procedure call depth exceeded")
