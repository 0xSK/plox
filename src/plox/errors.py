from abc import ABC
from plox.ptoken import PToken, PTokenType


class PloxErrorBase(Exception, ABC):
    """Base class for all Lox-related errors."""
    def __init__(self, message: str, token: PToken | None = None) -> None:
        self.message = message
        self.token = token
        super().__init__(self.__str__())

    def __str__(self) -> str:
        if self.token:
            if self.token.type == PTokenType.EOF:
                return f"[line {self.token.line}] Error at end: {self.message}"
            else:
                return f"[line {self.token.line}] Error at '{self.token.lexeme}': {self.message}"
        return self.message


class PloxSyntaxError(PloxErrorBase):
    """Errors detected during scanning/parsing."""
    pass

class PloxNotImplementedError(PloxErrorBase):
    """Errors detected during scanning/parsing."""
    pass
