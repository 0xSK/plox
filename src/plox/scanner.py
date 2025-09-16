from plox.token import Token, TokenType
from plox.logger import error
from typing import Any


class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

        self.scan_tokens()

    def scan_tokens(self) -> None:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(type=TokenType.EOF, lexeme="", literal=None, line=self.line)
        )

    def scan_token(self) -> None:
        currChar: str = self.advance()
        match currChar:
            case "(":
                self.add_token_simple(TokenType.LEFT_PAREN)
            case ")":
                self.add_token_simple(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token_simple(TokenType.LEFT_BRACE)
            case "}":
                self.add_token_simple(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token_simple(TokenType.COMMA)
            case ".":
                self.add_token_simple(TokenType.DOT)
            case "-":
                self.add_token_simple(TokenType.MINUS)
            case "+":
                self.add_token_simple(TokenType.PLUS)
            case ";":
                self.add_token_simple(TokenType.SEMICOLON)
            case "*":
                self.add_token_simple(TokenType.STAR)
            case "!":
                if self.match("="):
                    self.add_token_simple(TokenType.BANG_EQUAL)
                else:
                    self.add_token_simple(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token_simple(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token_simple(TokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token_simple(TokenType.LESS_EQUAL)
                else:
                    self.add_token_simple(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token_simple(TokenType.GREATER_EQUAL)
                else:
                    self.add_token_simple(TokenType.GREATER)
            case "/":
                # see if this is divide or a line comment
                if self.match("/"):
                    # this is a line comment, ignore everything until the end of the line
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    # this is a divide
                    self.add_token_simple(TokenType.SLASH)
            # beginning of a string
            case '"':
                self.parse_string()
            # beginning of a number
            case _ if "0" <= currChar <= "9":
                self.parse_number()
            # ignored whitespace
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case _:
                self.add_token_simple(TokenType.UNIMPLEMENTED)

    def advance(self) -> str:
        """
        returns the character at the `current` index,
        and increments the `current` index
        """
        curr_char = self.source[self.current]
        self.current += 1
        return curr_char

    def peek(self, ahead: int = 0) -> str:
        """
        returns the character at the `current` + `ahead` index,
        *without* incrementing the `current` index
        """
        if self.current + ahead >= len(self.source):
            return "\0"
        return self.source[self.current + ahead]

    def match(self, expectedChar: str) -> bool:
        if self.is_at_end():
            return False
        if self.peek() == expectedChar:
            self.advance()
            return True
        else:
            return False

    def add_token_simple(self, tokenType: TokenType) -> None:
        self.add_token_literal(tokenType=tokenType, literal=None)

    def add_token_literal(self, tokenType: TokenType, literal: Any) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(
            Token(type=tokenType, lexeme=lexeme, literal=literal, line=self.line)
        )

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def character_is_digit(self, char: str) -> bool:
        return "0" <= char <= "9"

    def parse_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error(self.line, "Unterminated string")
            return

        # get the closing "
        self.advance()

        stringVal: str = self.source[self.start + 1 : self.current - 1]
        self.add_token_literal(tokenType=TokenType.STRING, literal=stringVal)

    def parse_number(self) -> None:
        while self.character_is_digit(self.peek()):
            self.advance()

        # handle a decimal in the number
        if self.peek() == "." and self.character_is_digit(self.peek(1)):
            self.advance()
            while self.character_is_digit(self.peek()):
                self.advance()

        numberVal: float = float(self.source[self.start : self.current])
        self.add_token_literal(tokenType=TokenType.NUMBER, literal=numberVal)
