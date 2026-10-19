import os
from collections.abc import Generator
from pathlib import Path
from typing import cast

from syntactes import Grammar, LR1Parser, Symbol, Token
from syntactes.parser import Location

from pl0.parser.ast import *
from pl0.scanner.scanner import scanner

config_path = Path(os.path.realpath(os.path.dirname(__file__))) / Path(
    "config.syntactes"
)

with open(config_path, "r") as f:
    grammar = Grammar.from_text(f.read())

parser = LR1Parser.from_grammar(grammar)


@parser.execute_on("program -> block DOT")
def program(block, _dot):
    return Program(block.value)


@parser.execute_on("block -> assignments declarations procedures statement")
def block(assignments, declarations, procedures, statement):
    return Block(
        assignments.value, declarations.value, procedures.value, statement.value
    )


@parser.execute_on("assignments ->")
def empty_assignments():
    return []


@parser.execute_on("assignments -> CONST assign_list SEMICOLON")
def assignments(_const, assign_list, _semicolon):
    return assign_list.value


@parser.execute_on("assign_list -> assign")
def single_assignment(assign):
    return [assign.value]


@parser.execute_on("assign_list -> assign COMMA assign_list")
def multiple_assignments(assign, _comma, assign_list):
    return [assign.value] + assign_list.value


@parser.execute_on("assign -> ID EQ INT")
def assignment(var_id, _eq, literal):
    return Assignment(var_id.value, int(literal.value))


@parser.execute_on("declarations ->")
def empty_declarations():
    return []


@parser.execute_on("declarations -> VAR ID SEMICOLON")
def single_declaration(_var, var_id, _semicolon):
    return [Declaration(var_id.value)]


@parser.execute_on("declarations -> VAR ID COMMA id_list SEMICOLON")
def multiple_declarations(_var, var_id, _comma, id_list, _semicolon):
    return [Declaration(variable) for variable in [var_id.value] + id_list.value]


@parser.execute_on("id_list -> ID")
def single_id(var_id):
    return [var_id.value]


@parser.execute_on("id_list -> ID COMMA id_list")
def multiple_ids(var_id, _comma, id_list):
    return [var_id.value] + id_list.value


@parser.execute_on("procedures ->")
def empty_procedures():
    return []


@parser.execute_on("procedures -> procedure procedures")
def multiple_procedures(procedure, procedures):
    return [procedure.value] + procedures.value


@parser.execute_on("procedure -> PROCEDURE ID SEMICOLON block SEMICOLON")
def procedure(_proc, proc_id, _semicolon1, block, _semicolon2):
    return Procedure(proc_id.value, block.value)


@parser.execute_on("statement ->")
def empty_statement():
    return None


@parser.execute_on("statement -> assign_stm")
def assign_statement(assign_stm):
    return assign_stm.value


@parser.execute_on("statement -> call_stm")
def call_statement(call_stm):
    return call_stm.value


@parser.execute_on("statement -> read_stm")
def read_statement(read_stm):
    return read_stm.value


@parser.execute_on("statement -> write_stm")
def write_statement(write_stm):
    return write_stm.value


@parser.execute_on("statement -> begin_stm")
def begin_statement(begin_stm):
    return begin_stm.value


@parser.execute_on("statement -> if_stm")
def if_statement(if_stm):
    return if_stm.value


@parser.execute_on("statement -> while_stm")
def while_statement(while_stm):
    return while_stm.value


@parser.execute_on("assign_stm -> ID ASSIGN expression")
def assign_stm(var_id, _assign, expression):
    return AssignStatement(var_id.value, expression.value)


@parser.execute_on("call_stm -> CALL ID")
def call_stm(_call, proc_id):
    return CallStatement(proc_id.value)


@parser.execute_on("read_stm -> QMARK ID")
def read_stm(_qmark, var_id):
    return ReadStatement(var_id.value)


@parser.execute_on("write_stm -> BANG expression")
def write_stm(_bang, expression):
    return WriteStatement(expression.value)


@parser.execute_on("begin_stm -> BEGIN statement_list END")
def begin_stm(_begin, statement_list, _end):
    return BeginStatement(statement_list.value)


@parser.execute_on("statement_list -> statement")
def single_statement_list(statement):
    return [statement.value]


@parser.execute_on("statement_list -> statement SEMICOLON statement_list")
def multiple_statement_list(statement, _semicolon, statement_list):
    return [statement.value] + statement_list.value


@parser.execute_on("if_stm -> IF condition THEN statement")
def if_stm(_if, condition, _then, statement):
    return IfStatement(condition.value, statement.value)


@parser.execute_on("while_stm -> WHILE condition DO statement")
def while_stm(_while, condition, _do, statement):
    return WhileStatement(condition.value, statement.value)


@parser.execute_on("condition -> ODD expression")
def odd_condition(_odd, expression):
    return Condition(Operator.ODD, expression.value, None)


@parser.execute_on("condition -> expression EQ expression")
def eq_condition(left, _eq, right):
    return Condition(Operator.EQ, left.value, right.value)


@parser.execute_on("condition -> expression HASH expression")
def hash_condition(left, _hash, right):
    return Condition(Operator.HASH, left.value, right.value)


@parser.execute_on("condition -> expression LT expression")
def lt_condition(left, _lt, right):
    return Condition(Operator.LT, left.value, right.value)


@parser.execute_on("condition -> expression LE expression")
def le_condition(left, _le, right):
    return Condition(Operator.LE, left.value, right.value)


@parser.execute_on("condition -> expression GT expression")
def gt_condition(left, _gt, right):
    return Condition(Operator.GT, left.value, right.value)


@parser.execute_on("condition -> expression GE expression")
def ge_condition(left, _ge, right):
    return Condition(Operator.GE, left.value, right.value)


@parser.execute_on("expression -> signed_or_unsigned_term multiple_term_list")
def expression(term, term_list):
    return Expression(term.value, term_list.value)


@parser.execute_on("multiple_term_list -> ")
def empty_term_list():
    return []


@parser.execute_on("multiple_term_list -> non_empty_term_list")
def non_empty_term_list(term_list):
    return term_list.value


@parser.execute_on("non_empty_term_list -> signed_term")
def single_signed_term(signed_term):
    return [signed_term.value]


@parser.execute_on("non_empty_term_list -> signed_term non_empty_term_list")
def multiple_signed_terms(signed_term, term_list):
    return [signed_term.value] + term_list.value


@parser.execute_on("signed_term -> PLUS term")
def plus_term(_plus, term):
    return SignedTerm(term.value, UnaryOp.PLUS)


@parser.execute_on("signed_term -> MINUS term")
def minus_term(_minus, term):
    return SignedTerm(term.value, UnaryOp.MINUS)


@parser.execute_on("signed_or_unsigned_term -> term")
def unsigned_term(term):
    return SignedOrUnsignedTerm(term.value, None)


@parser.execute_on("signed_or_unsigned_term -> signed_term")
def signed_term(signed_term):
    return SignedOrUnsignedTerm(signed_term.value.term, signed_term.value.unary_op)


@parser.execute_on("term -> factor")
def single_factor_term(factor):
    return factor.value


@parser.execute_on("term -> term MULT factor")
def mult_term(left, _mult, right):
    return BinaryTerm(TermOperator.MULT, left.value, right.value)


@parser.execute_on("term -> term DIV factor")
def div_term(left, _div, right):
    return BinaryTerm(TermOperator.DIV, left.value, right.value)


@parser.execute_on("factor -> ID")
def variable_factor(var_id):
    return Variable(var_id.value)


@parser.execute_on("factor -> INT")
def literal_factor(literal):
    return Number(int(literal.value))


@parser.execute_on("factor -> LPAREN expression RPAREN")
def expression_factor(_lparen, expression, _rparen):
    return expression.value


def parse(text: str) -> Program:
    return cast(Program, parser.parse(tokens(text)))


def tokens(text: str) -> Generator[Token]:
    """
    Scan the text and yield its tokens as syntactes tokens, ending with EOF.
    """
    for token in scanner.scan(text):
        yield Token(
            Symbol(token.name, is_terminal=True),
            Location.from_object(token.location),
            token.literal,
        )

    line_start = text.rfind("\n") + 1
    end = Location(len(text), text.count("\n") + 1, len(text) - line_start + 1)
    yield Token(Symbol.eof(), end)
