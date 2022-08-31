from lexer.lexer import Lexer
from lexer.tokens import Token

def types(tokens: list[Token], expected: list[str]) -> None:
    """Check that the tokens have the expected types."""
    assert [token.type for token in tokens] == expected


def values(tokens: list[Token], expected: list[str]) -> None:
    """Check that the tokens have the expected values."""
    assert [token.value for token in tokens] == expected


def pos(tokens: list[Token], expected: list[int]) -> None:
    """Check that the tokens have the expected positions."""
    assert [token.pos for token in tokens] == expected


def test_binop():
    tokens = list(Lexer("1 + 2"))
    types(tokens, ["int", "op", "int"])
    values(tokens, ["1", "+", "2"])
    pos(tokens, [0, 2, 4])


def test_assign():
    tokens = list(Lexer("x = 1"))
    types(tokens, ["id", "assign", "int"])
    values(tokens, ["x", "=", "1"])
    pos(tokens, [0, 2, 4])


def test_parens():
    tokens = list(Lexer("(1 + 2)"))
    types(tokens, ["paren", "int", "op", "int", "paren"])
    values(tokens, ["(", "1", "+", "2", ")"])
    pos(tokens, [0, 1, 3, 5, 6])


def test_complex():
    tokens = list(Lexer("ab1 = 1 - (1 / bc) + 2"))
    types(tokens, ['id', 'assign', 'int', 'op', 'paren', 'int', 'op', 'id', 'paren', 'op', 'int'])
    values(tokens, ['ab1', '=', '1', '-', '(', '1', '/', 'bc', ')', '+', '2'])