from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable
from dataclasses import dataclass
from plox.ptoken import PToken


class Expr(ABC):
    @abstractmethod
    def accept[T](self, visitor: Visitor[T]) -> T:
        pass


@dataclass
class AssignExpr(Expr):
    name: PToken
    value: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_assign_expression(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expression(self)


@dataclass
class LiteralExpr(Expr):
    value: Any

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expression(self)


@dataclass
class UnaryExpr(Expr):
    operator: PToken
    right: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expression(self)


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: PToken
    right: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expression(self)


@runtime_checkable
class Visitor[R](Protocol):
    def visit_assign_expression(self, expr: AssignExpr) -> R: ...
    def visit_grouping_expression(self, expr: GroupingExpr) -> R: ...
    def visit_literal_expression(self, expr: LiteralExpr) -> R: ...
    def visit_unary_expression(self, expr: UnaryExpr) -> R: ...
    def visit_binary_expression(self, expr: BinaryExpr) -> R: ...


class AstPrinter(Visitor[str]):
    def pformat(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_assign_expression(self, expr: AssignExpr) -> str:
        return self.parenthesize(f"{expr.name}=", expr.value)

    def visit_grouping_expression(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expression(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visit_unary_expression(self, expr: UnaryExpr) -> str:
        return self.parenthesize(str(expr.operator.lexeme), expr.right)
    
    def visit_binary_expression(self, expr: BinaryExpr) -> str:
        return self.parenthesize(str(expr.operator.lexeme), expr.left, expr.right)
    
    def parenthesize(self, name: str, *expressions: Expr):
        s = f"({name}"
        for expression in expressions:
            s += f" {expression.accept(self)}"
        s += ")"
        return s
