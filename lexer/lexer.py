"""
    A lexer is an iterator over the tokens of a program.
"""

from typing import Callable, Iterator
from lexer.tokens import Token


class Lexer(Iterator):
    """An Iterator over the tokens of a calc program."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.cur_token = self._next_token()
    

    def _peek_char(self) -> str | None:
        """Return the next character in the text, or None if there isn't one."""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    

    def _next_char(self) -> str | None:
        """Return the next character in the text, and advance the position."""
        char = self._peek_char()
        if char is not None:
            self.pos += 1
        return char

    
    def consume_while(self, predicate: Callable[[str], bool]) -> str:
        """Consume characters from the text while the predicate is true."""
        start = self.pos
        while self._peek_char() is not None and predicate(self._peek_char()):
            self._next_char()
        return self.text[start:self.pos]


    def _next_token(self) -> Token | None:
        """Parse the next token from the text."""
        self.consume_while(str.isspace)
        start = self.pos
        char = self._peek_char()
        if char is None:
            return None
        if char.isdigit():
            return Token("int", self.consume_while(str.isdigit), start)
        if char.isalpha():
            return Token("id", self.consume_while(str.isalnum), start)
        if char in "+-*/":
            return Token("op", self._next_char(), start)
        if char == '=':
            return Token("assign", self._next_char(), start)
        if char in '()':
            return Token("paren", self._next_char(), start)
        raise ValueError(f"Unexpected character {char} at position {self.pos}")
    

    def peek(self) -> Token | None:
        """Return the next token without consuming it."""
        return self.cur_token
    

    def next(self) -> Token | None:
        """Return the next token and advance the lexer."""
        return next(self)


    def __iter__(self) -> 'Lexer':
        return self
    

    def __next__(self) -> Token:
        if self.cur_token is None:
            raise StopIteration
        token = self.cur_token
        self.cur_token = self._next_token()
        return token