from lexer.lexer import Lexer
from parser.ast import *
from parser.parser import parse


def flatten_ast(ast: AST) -> list[type]:
    """Flatten an AST into a list of types in in-order."""
    if isinstance(ast, Program):
        assigns = []
        for assign in ast.statements:
            assigns.extend(flatten_ast(assign))
        return [Program] + assigns
    elif isinstance(ast, Assign):
        return flatten_ast(ast.id) + [Assign] + flatten_ast(ast.expr)
    elif isinstance(ast, Id):
        return [Id]
    elif isinstance(ast, BinOp):
        return flatten_ast(ast.left) + [BinOp] + flatten_ast(ast.right)
    elif isinstance(ast, UnaryOp):
        return [UnaryOp] + flatten_ast(ast.expr)
    elif isinstance(ast, Int):
        return [Int]
    else:
        raise TypeError(f"Unknown type: {type(ast)}")


def has_types(ast: AST, types: list[type]) -> None:
    """Assert that the AST has the given types."""
    assert flatten_ast(ast) == types


def test_parser() -> None:
    ast = parse(Lexer("a = 1 + 2"))
    has_types(ast, [Program, Id, Assign, Int, BinOp, Int])


def test_complex() -> None:
    lexer = Lexer("a = 1 + (b2/3) - -4 * (--1)")
    ast = parse(lexer)
    has_types(ast, [Program, Id, Assign, Int, BinOp, Id, BinOp, Int, BinOp, UnaryOp, Int, BinOp, UnaryOp, UnaryOp, Int])
