from __future__ import annotations

from dataclasses import dataclass, field

from pl0.evaluator.errors import DuplicateNameError, NameKindError, UndefinedNameError
from pl0.parser.ast import Procedure


@dataclass
class Closure:
    """
    A procedure and the environment it was declared in, which its body sees.
    """

    procedure: Procedure
    env: Environment


@dataclass
class Environment:
    """
    The names declared by one block. Lookups that miss go to the parent, the
    environment of the enclosing block, so inner names shadow outer ones.
    """

    parent: Environment | None = None
    constants: dict[str, int] = field(default_factory=dict)
    variables: dict[str, int] = field(default_factory=dict)
    procedures: dict[str, Closure] = field(default_factory=dict)

    def declare_constant(self, name: str, value: int) -> None:
        self._check_undeclared(name)
        self.constants[name] = value

    def declare_variable(self, name: str) -> None:
        self._check_undeclared(name)
        self.variables[name] = 0

    def declare_procedure(self, procedure: Procedure) -> None:
        self._check_undeclared(procedure.name)
        self.procedures[procedure.name] = Closure(procedure, self)

    def value(self, name: str) -> int:
        """
        Returns the value of the constant or variable `name`.
        """
        scope = self._scope(name)
        if name in scope.constants:
            return scope.constants[name]

        if name in scope.variables:
            return scope.variables[name]

        raise NameKindError(name, scope._kind(name), "constant or variable")

    def assign(self, name: str, value: int) -> None:
        """
        Sets the variable `name` to `value`, in the scope that declares it.
        """
        self._variable_scope(name).variables[name] = value

    def check_variable(self, name: str) -> None:
        """
        Raises unless `name` is a variable, so it can be assigned.
        """
        self._variable_scope(name)

    def procedure(self, name: str) -> Closure:
        scope = self._scope(name)
        if name not in scope.procedures:
            raise NameKindError(name, scope._kind(name), "procedure")

        return scope.procedures[name]

    def _scope(self, name: str) -> Environment:
        """
        Returns the innermost environment that declares `name`.
        """
        env: Environment | None = self
        while env is not None:
            if env._declares(name):
                return env

            env = env.parent

        raise UndefinedNameError(name)

    def _variable_scope(self, name: str) -> Environment:
        scope = self._scope(name)
        if name not in scope.variables:
            raise NameKindError(name, scope._kind(name), "variable")

        return scope

    def _declares(self, name: str) -> bool:
        return (
            name in self.constants or name in self.variables or name in self.procedures
        )

    def _kind(self, name: str) -> str:
        if name in self.constants:
            return "constant"

        if name in self.variables:
            return "variable"

        return "procedure"

    def _check_undeclared(self, name: str) -> None:
        if self._declares(name):
            raise DuplicateNameError(name)
