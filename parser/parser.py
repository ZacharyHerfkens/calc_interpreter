"""
    A recursive descent parser for the calc language. 

    The grammar is as follows:
        program: { assign } EOF
        assign: id '=' add
        add: mul { ('+' | '-') mul }
        mul: unary { ('*' | '/') unary }
        unary: ('+' | '-') unary | term
        term: int | id | '(' add ')'
"""

from lexer.lexer import Lexer
from lexer.tokens import Token
from parser.ast import *


class SyntaxError(Exception):
    """An error that occurs during parsing."""
    
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(f"SyntaxError: {message}")
        self.token = token


def _expect(lexer: Lexer, token_type: str, value: str | None = None) -> Token:
    """Expect a token of a certain type and value from the lexer."""
    tok = lexer.peek()
    if tok is None:
        raise SyntaxError(f"Expected {token_type} but got EOF", tok)
    if tok.type != token_type:
        raise SyntaxError(f"Expected {token_type}, got {tok.type}", tok)
    if value is not None and tok.value != value:
        raise SyntaxError(f"Expected {value}, got {tok.value}", tok)
    
    return lexer.next()


def _has(lexer: Lexer, token_type: str, value: str | None = None) -> bool:
    """Check if the next token is of a certain type and value."""
    tok = lexer.peek()
    return tok is not None and tok.type == token_type and (value is None or tok.value == value)


def _term(lexer: Lexer) -> Expr:
    """Parse a term."""
    if _has(lexer, "int"):
        tok = lexer.next()
        return Int(int(tok.value))
    elif _has(lexer, "id"):
        tok = lexer.next()
        return Id(tok.value)
    elif _has(lexer, "paren", "("):
        lexer.next()
        expr = _add(lexer)
        _expect(lexer, "paren", ")")
        return expr
    
    raise SyntaxError(f"Expected int, id, or '(' - got {lexer.peek().value}", lexer.peek())


def _unary(lexer: Lexer) -> Expr:
    """Parse a unary expression."""
    if _has(lexer, "op", "+") or _has(lexer, "op", "-"):
        op = lexer.next()
        expr = _unary(lexer)
        return UnaryOp(op.value, expr)
    
    return _term(lexer)

def _mul(lexer: Lexer) -> Expr:
    """Parse a multiplication expression."""
    left = _unary(lexer)
    while _has(lexer, "op", "*") or _has(lexer, "op", "/"):
        op = lexer.next()
        right = _unary(lexer)
        left = BinOp(left, op.value, right)
    
    return left


def _add(lexer: Lexer) -> Expr:
    """Parse an addition expression."""
    left = _mul(lexer)
    while _has(lexer, "op", "+") or _has(lexer, "op", "-"):
        op = lexer.next()
        right = _mul(lexer)
        left = BinOp(left, op.value, right)
    
    return left


def _assign(lexer: Lexer) -> Assign:
    """Parse an assignment statement."""
    id = _expect(lexer, "id")
    _expect(lexer, "assign")
    expr = _add(lexer)
    return Assign(Id(id.value), expr)


def _program(lexer: Lexer) -> Program:
    """Parse a program."""
    statements = []
    while lexer.peek() is not None:
        statements.append(_assign(lexer))
    
    return Program(statements)


def parse(lexer: Lexer) -> Program:
    """Parse the tokens produced by the lexer into an AST."""
    return _program(lexer)