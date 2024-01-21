from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    EOF = -1
    EOL = 0
    NEWLINE = 1
    IDENTIFIER = 2
    COMA = 3
    # Types
    INT = 101
    FLOAT = 102
    STRING = 103
    BOOL = 104
    # Keywords
    DEF = 201
    RETURN = 202
    ENUM = 203
    STRUCT = 204
    IMPORT = 205
    FEATURE = 206
    # Operators
    PLUS = 301
    MINUS = 302
    MULTIPLY = 303
    DIVIDE = 304
    TYPEOF = 305
    EQUALS = 306
    MORETHAN = 307
    LESSTHAN = 308
    COLON = 309
    DOT = 310
    # Brackets
    LPAREN = 401
    RPAREN = 402
    LBRACE = 403
    RBRACE = 404
    LSQUARE = 405
    RSQUARE = 406


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"{self.type}  :  \"{self.value}\" @ {self.line}:{self.column}"

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 2XX.
            if kind.name.lower() == tokenText.lower() and 200 <= kind.value < 300:
                return kind
        return None

    @staticmethod
    def checkIfType(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 2XX.
            if kind.name.lower() == tokenText.lower() and 100 <= kind.value < 200:
                return kind
        return None
