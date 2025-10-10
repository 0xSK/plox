from enum import Enum, auto
from typing import Any

class PTokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    
    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    
    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    
    # Special tokens.
    EOF = auto()

    # only while in development
    UNIMPLEMENTED = auto()

class PToken:
    def __init__(self, 
        type: PTokenType, 
        lexeme: str, 
        literal: Any, 
        line: int
    ) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str: return f"<{self.type}> {self.lexeme} {self.literal}"
    def __repr__(self) -> str: return self.__str__()
