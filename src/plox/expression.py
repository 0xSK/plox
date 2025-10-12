from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable
from functools import singledispatchmethod
from dataclasses import dataclass
from plox.ptoken import PToken


class Expr(ABC):
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit(self)


@dataclass
class AssignExpr(Expr):
    name: PToken
    value: Expr


@dataclass
class GroupingExpr(Expr):
    expression: Expr


@dataclass
class LiteralExpr(Expr):
    value: Any


@dataclass
class UnaryExpr(Expr):
    operator: PToken
    right: Expr


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: PToken
    right: Expr


@runtime_checkable
class Visitor[R](Protocol):
    def visit(self, expr: Expr) -> R: ...


class AstPrinter(Visitor[str]):
    def pformat(self, expr: Expr) -> str:
        return expr.accept(self)

    @singledispatchmethod
    def visit(self, expr: Expr) -> str:
        raise NotImplementedError(
            f"The `visit` dispatcher for {type(expr)} objects is not defined"
        )

    @visit.register
    def _(self, expr: AssignExpr) -> str:
        return self.parenthesize(f"{expr.name}=", expr.value)

    @visit.register
    def _(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    @visit.register
    def _(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    @visit.register
    def _(self, expr: UnaryExpr) -> str:
        return self.parenthesize(str(expr.operator.lexeme), expr.right)

    @visit.register
    def _(self, expr: BinaryExpr) -> str:
        return self.parenthesize(str(expr.operator.lexeme), expr.left, expr.right)

    def parenthesize(self, name: str, *expressions: Expr):
        s = f"({name}"
        for expression in expressions:
            s += f" {expression.accept(self)}"
        s += ")"
        return s
