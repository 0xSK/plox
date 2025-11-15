from plox.expression import (
    Visitor,
    Expr,
    LiteralExpr,
    GroupingExpr,
    UnaryExpr,
    BinaryExpr,
)
from plox.ptoken import PTokenType, PToken
from functools import singledispatchmethod
from plox.errors import PloxRuntimeError
from plox.logger import error
from typing import TypeGuard


class Interpreter(Visitor[object]):
    def interpret(self, expr: Expr) -> None:
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except PloxRuntimeError as e:
            error(e.token.line if e.token is not None else None, e.message)

    def stringify(self, value: object) -> str:
        if value is None:
            return "nil"
        return str(value)

    @singledispatchmethod
    def visit(self, expr: Expr) -> object:
        raise NotImplementedError(
            f"The `visit` dispatcher for {type(expr)} objects is not defined"
        )

    @visit.register
    def _(self, expr: LiteralExpr) -> object:
        return expr.value

    @visit.register
    def _(self, expr: GroupingExpr) -> object:
        return self.evaluate(expr.expression)
        # FIXME: also try:
        # return self.visit(expr.expression)

    @visit.register
    def _(self, expr: UnaryExpr) -> object:
        rightObj = self.evaluate(expr.right)

        match expr.operator.type:
            case PTokenType.MINUS:
                if self.check_number_operand(rightObj, expr.operator):
                    return -rightObj
            case PTokenType.BANG:
                return not self.is_truthy(rightObj)
            case _:
                raise ValueError(
                    "Invalid unary operator type parsed, "
                    "this is an error in Plox implementation",
                    expr.operator,
                )

    @visit.register
    def _(self, expr: BinaryExpr) -> object:
        leftObj = self.evaluate(expr.left)
        rightObj = self.evaluate(expr.right)

        match expr.operator.type:
            case PTokenType.MINUS:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj - rightObj
            case PTokenType.SLASH:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj / rightObj
            case PTokenType.STAR:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj * rightObj
            case PTokenType.PLUS:
                if isinstance(leftObj, float) and isinstance(rightObj, float):
                    return leftObj + rightObj
                elif isinstance(leftObj, str) and isinstance(rightObj, str):
                    return leftObj + rightObj
                else:
                    raise PloxRuntimeError(
                        "Illegal combination of operarands", expr.operator
                    )
            case PTokenType.GREATER:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj > rightObj
            case PTokenType.GREATER_EQUAL:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj >= rightObj
            case PTokenType.LESS:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj < rightObj
            case PTokenType.LESS_EQUAL:
                if self.check_number_operand(leftObj, expr.operator):
                    if self.check_number_operand(rightObj, expr.operator):
                        return leftObj <= rightObj
            case PTokenType.EQUAL_EQUAL:
                return self.is_equal(leftObj, rightObj)
            case PTokenType.BANG_EQUAL:
                return not self.is_equal(leftObj, rightObj)
            case _:
                raise ValueError(
                    "Invalid binary operator type parsed, "
                    "this is an error in Plox implementation",
                    expr.operator,
                )

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, object) -> bool:
        # Lox follows Ruby’s simple rule: false and nil are falsey, and everything else is truthy.
        if object is None:
            return False
        if isinstance(object, bool):
            return object
        return True

    def is_equal(self, left: object, right: object) -> bool:
        return type(left) is type(right) and left == right

    def check_number_operand(
        self, operand: object, operator: PToken
    ) -> TypeGuard[float]:
        if not isinstance(operand, float):
            raise PloxRuntimeError("Operand must be a number", operator)
        return True
