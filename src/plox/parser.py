from plox.ptoken import PToken, PTokenType
from plox.expression import Expr, BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from plox.errors import PloxSyntaxError


class Parser:
    """
    Parses a list of tokens into an expression

    It implements a parser for this grammar:
    expression     → equality
    equality       → comparison ( ( "!=" | "==" ) comparison )*
    comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )*
    term           → factor ( ( "-" | "+" ) factor )*
    factor         → unary ( ( "/" | "*" ) unary )*
    unary          → ( "!" | "-" ) unary | primary
    primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"
    """

    def __init__(self, tokens: list[PToken]) -> None:
        self.tokens: list[PToken] = tokens
        self.curr: int = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(PTokenType.EQUAL_EQUAL, PTokenType.BANG_EQUAL):
            operator: PToken = self.prev()
            right_expr = self.comparison()
            expr = BinaryExpr(left=expr, operator=operator, right=right_expr)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()

        while self.match(
            PTokenType.GREATER,
            PTokenType.GREATER_EQUAL,
            PTokenType.LESS,
            PTokenType.LESS_EQUAL,
        ):
            operator: PToken = self.prev()
            right_expr = self.term()
            expr = BinaryExpr(left=expr, operator=operator, right=right_expr)

        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self.match(PTokenType.MINUS, PTokenType.PLUS):
            operator: PToken = self.prev()
            right_expr = self.factor()
            expr = BinaryExpr(left=expr, operator=operator, right=right_expr)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self.match(PTokenType.STAR, PTokenType.SLASH):
            operator: PToken = self.prev()
            right_expr = self.unary()
            expr = BinaryExpr(left=expr, operator=operator, right=right_expr)

        return expr

    def unary(self) -> Expr:
        if self.match(PTokenType.BANG, PTokenType.MINUS):
            operator: PToken = self.prev()
            right_expr = self.unary()
            return UnaryExpr(operator=operator, right=right_expr)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(PTokenType.FALSE):
            return LiteralExpr(False)
        if self.match(PTokenType.TRUE):
            return LiteralExpr(True)
        if self.match(PTokenType.NIL):
            return LiteralExpr(None)
        if self.match(PTokenType.NUMBER, PTokenType.STRING):
            return LiteralExpr(self.prev().literal)
        if self.match(PTokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(PTokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return GroupingExpr(expr)
        raise PloxSyntaxError('Expected expression', self.peek())

    def match(self, *types: PTokenType):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, tokenType: PTokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == tokenType

    def advance(self) -> PToken:
        if not self.is_at_end():
            self.curr += 1
        return self.prev()

    def is_at_end(self) -> bool:
        return self.peek().type == PTokenType.EOF

    def peek(self) -> PToken:
        return self.tokens[self.curr]

    def prev(self) -> PToken:
        if self.curr == 0:
            raise IndexError("Called prev() on first token")
        return self.tokens[self.curr - 1]

    def consume(self, tokenType: PTokenType, message: str) -> PToken:
        if self.check(tokenType):
            return self.advance()
        raise PloxSyntaxError(message, self.peek())

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.prev().type == PTokenType.SEMICOLON:
                return

            elif self.peek().type in [
                PTokenType.CLASS,
                PTokenType.FUN,
                PTokenType.VAR,
                PTokenType.FOR,
                PTokenType.IF,
                PTokenType.WHILE,
                PTokenType.PRINT,
                PTokenType.RETURN,
            ]:
                return
            else:
                self.advance()
    
    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except PloxSyntaxError as e:
            print(e)
            return None
