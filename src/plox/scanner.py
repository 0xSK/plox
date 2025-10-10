from plox.ptoken import PToken, PTokenType
from plox.logger import error
from typing import Any


class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[PToken] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

        self.scan_tokens()

    def scan_tokens(self) -> None:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            PToken(type=PTokenType.EOF, lexeme="", literal=None, line=self.line)
        )

    def scan_token(self) -> None:
        currChar: str = self.advance()
        match currChar:
            case "(":
                self.add_token_simple(PTokenType.LEFT_PAREN)
            case ")":
                self.add_token_simple(PTokenType.RIGHT_PAREN)
            case "{":
                self.add_token_simple(PTokenType.LEFT_BRACE)
            case "}":
                self.add_token_simple(PTokenType.RIGHT_BRACE)
            case ",":
                self.add_token_simple(PTokenType.COMMA)
            case ".":
                self.add_token_simple(PTokenType.DOT)
            case "-":
                self.add_token_simple(PTokenType.MINUS)
            case "+":
                self.add_token_simple(PTokenType.PLUS)
            case ";":
                self.add_token_simple(PTokenType.SEMICOLON)
            case "*":
                self.add_token_simple(PTokenType.STAR)
            case "!":
                if self.match("="):
                    self.add_token_simple(PTokenType.BANG_EQUAL)
                else:
                    self.add_token_simple(PTokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token_simple(PTokenType.EQUAL_EQUAL)
                else:
                    self.add_token_simple(PTokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token_simple(PTokenType.LESS_EQUAL)
                else:
                    self.add_token_simple(PTokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token_simple(PTokenType.GREATER_EQUAL)
                else:
                    self.add_token_simple(PTokenType.GREATER)
            case "/":
                # see if this is divide or a line comment
                if self.match("/"):
                    # this is a line comment, ignore everything until the end of the line
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    # this is a divide
                    self.add_token_simple(PTokenType.SLASH)
            # beginning of a string
            case '"':
                self.parse_string()
            # beginning of a number
            case _ if "0" <= currChar <= "9":
                self.parse_number()
            # beginning of an identifier
            case _ if self.character_is_alpha(currChar):
                self.parse_identifier()
            # ignored whitespace
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case _:
                self.add_token_simple(PTokenType.UNIMPLEMENTED)

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

    def add_token_simple(self, tokenType: PTokenType) -> None:
        self.add_token_literal(tokenType=tokenType, literal=None)

    def add_token_literal(self, tokenType: PTokenType, literal: Any) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(
            PToken(type=tokenType, lexeme=lexeme, literal=literal, line=self.line)
        )

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def character_is_digit(self, char: str) -> bool:
        return "0" <= char <= "9"

    def character_is_alpha(self, char: str) -> bool:
        return ("a" <= char <= "z") or ("A" <= char <= "Z") or char == "_"

    def character_is_alphanumeric(self, char: str) -> bool:
        return self.character_is_alpha(char) or self.character_is_digit(char)

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
        self.add_token_literal(tokenType=PTokenType.STRING, literal=stringVal)

    def parse_number(self) -> None:
        while self.character_is_digit(self.peek()):
            self.advance()

        # handle a decimal in the number
        if self.peek() == "." and self.character_is_digit(self.peek(1)):
            self.advance()
            while self.character_is_digit(self.peek()):
                self.advance()

        numberVal: float = float(self.source[self.start : self.current])
        self.add_token_literal(tokenType=PTokenType.NUMBER, literal=numberVal)

    def parse_identifier(self) -> None:
        while self.character_is_alphanumeric(self.peek()):
            self.advance()

        identifierName: str = self.source[self.start : self.current]
        reservedKeywords: list[str] = [
            "and",
            "class",
            "else",
            "false",
            "for",
            "fun",
            "if",
            "nil",
            "or",
            "print",
            "return",
            "super",
            "this",
            "true",
            "var",
            "while",
        ]
        if identifierName in reservedKeywords:
            tokenType = PTokenType[identifierName.upper()]
        else:
            tokenType = PTokenType.IDENTIFIER

        self.add_token_simple(tokenType)
