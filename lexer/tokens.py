"""
    The tokens needed by the lexer.
"""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Token:
    """Tokens are used by the lexer, and store a type, value, and location in the text."""
    type: str
    value: str
    pos: int

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', at {self.pos})"
    
    