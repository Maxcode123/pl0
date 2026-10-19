from collections.abc import Callable

from pl0.evaluator.env import Environment
from pl0.evaluator.errors import (
    DivisionByZeroError,
    InvalidInputError,
    RecursionDepthError,
)
from pl0.parser.ast import (
    AssignStatement,
    BeginStatement,
    BinaryTerm,
    Block,
    CallStatement,
    Condition,
    Expression,
    IfStatement,
    Number,
    Operator,
    Program,
    ReadStatement,
    Statement,
    Term,
    TermOperator,
    UnaryOp,
    Variable,
    WhileStatement,
    WriteStatement,
)


class Evaluator:
    """
    Runs a program's AST. `?` reads a line with `read` and `!` passes the value
    to `write`; they default to stdin and stdout.
    """

    def __init__(
        self,
        read: Callable[[], str] = input,
        write: Callable[[int], object] = print,
    ) -> None:
        self._read = read
        self._write = write

    def run(self, program: Program) -> None:
        """
        Raises a subclass of `pl0.evaluator.errors.EvalError` if the program
        fails at runtime.
        """
        try:
            self._block(program.block, Environment())
        except RecursionError:
            raise RecursionDepthError() from None

    def _block(self, block: Block, env: Environment) -> None:
        for assignment in block.assignments:
            env.declare_constant(assignment.variable, assignment.value)

        for declaration in block.declarations:
            env.declare_variable(declaration.variable)

        for procedure in block.procedures:
            env.declare_procedure(procedure)

        self._statement(block.statement, env)

    def _statement(self, statement: Statement | None, env: Environment) -> None:
        match statement:
            case None:
                pass
            case AssignStatement(variable, expression):
                env.check_variable(variable)
                env.assign(variable, self._expression(expression, env))
            case CallStatement(proc_name):
                closure = env.procedure(proc_name)
                self._block(closure.procedure.block, Environment(closure.env))
            case ReadStatement(variable):
                env.check_variable(variable)
                env.assign(variable, self._read_int())
            case WriteStatement(expression):
                self._write(self._expression(expression, env))
            case BeginStatement(statement_list):
                for inner in statement_list:
                    self._statement(inner, env)
            case IfStatement(condition, inner):
                if self._condition(condition, env):
                    self._statement(inner, env)
            case WhileStatement(condition, inner):
                while self._condition(condition, env):
                    self._statement(inner, env)

    def _condition(self, condition: Condition, env: Environment) -> bool:
        left = self._expression(condition.left, env)
        if condition.operator == Operator.ODD:
            return left % 2 != 0

        # Only ODD conditions have no right-hand side.
        assert condition.right is not None
        right = self._expression(condition.right, env)

        match condition.operator:
            case Operator.EQ:
                return left == right
            case Operator.HASH:
                return left != right
            case Operator.LT:
                return left < right
            case Operator.LE:
                return left <= right
            case Operator.GT:
                return left > right
            case Operator.GE:
                return left >= right

    def _expression(self, expression: Expression, env: Environment) -> int:
        first = expression.first_term
        value = self._term(first.term, env)
        if first.unary_op == UnaryOp.MINUS:
            value = -value

        for signed_term in expression.term_list:
            term = self._term(signed_term.term, env)
            if signed_term.unary_op == UnaryOp.PLUS:
                value += term
            else:
                value -= term

        return value

    def _term(self, term: Term, env: Environment) -> int:
        match term:
            case BinaryTerm(operator, left, right):
                left_value = self._term(left, env)
                right_value = self._term(right, env)
                if operator == TermOperator.MULT:
                    return left_value * right_value

                return _divide(left_value, right_value)
            case Variable(name):
                return env.value(name)
            case Number(value):
                return value
            case Expression():
                return self._expression(term, env)

    def _read_int(self) -> int:
        try:
            text = self._read()
        except EOFError:
            raise InvalidInputError(None) from None

        try:
            return int(text)
        except ValueError:
            raise InvalidInputError(text) from None


def _divide(left: int, right: int) -> int:
    """
    Integer division that truncates toward zero, unlike Python's `//`.
    """
    if right == 0:
        raise DivisionByZeroError()

    quotient = abs(left) // abs(right)
    return quotient if (left < 0) == (right < 0) else -quotient
