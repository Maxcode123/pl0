from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Assignment:
    variable: str
    value: int


@dataclass
class Declaration:
    variable: str


@dataclass
class Procedure:
    name: str
    block: Block


@dataclass
class AssignStatement:
    variable: str
    expression: Expression


@dataclass
class CallStatement:
    proc_name: str


@dataclass
class ReadStatement:
    variable: str


@dataclass
class WriteStatement:
    expression: Expression


@dataclass
class BeginStatement:
    statement_list: list[Statement]


@dataclass
class IfStatement:
    condition: Condition
    statement: Statement


@dataclass
class WhileStatement:
    condition: Condition
    statement: Statement


type Statement = (
    AssignStatement
    | CallStatement
    | ReadStatement
    | WriteStatement
    | BeginStatement
    | IfStatement
    | WhileStatement
)


@dataclass
class Condition:
    operator: Operator
    left: Expression
    right: Expression | None


class Operator(StrEnum):
    ODD = "ODD"
    EQ = "EQ"
    HASH = "HASH"
    LT = "LT"
    LE = "LE"
    GT = "GT"
    GE = "GE"


@dataclass
class Expression:
    first_term: SignedOrUnsignedTerm
    term_list: list[SignedTerm]


@dataclass
class SignedOrUnsignedTerm:
    term: Term
    unary_op: UnaryOp | None


class UnaryOp(StrEnum):
    PLUS = "PLUS"
    MINUS = "MINUS"


@dataclass
class SignedTerm:
    term: Term
    unary_op: UnaryOp


type Term = Factor | BinaryTerm


@dataclass
class BinaryTerm:
    operator: TermOperator
    left: Term
    right: Factor


class TermOperator(StrEnum):
    MULT = "MULT"
    DIV = "DIV"


type Factor = Variable | Number | Expression


@dataclass
class Variable:
    name: str


@dataclass
class Number:
    value: int


@dataclass
class Block:
    assignments: list[Assignment]
    declarations: list[Declaration]
    procedures: list[Procedure]
    statement: Statement | None


@dataclass
class Program:
    block: Block
