from lexer.lexer import Lexer, LexerError
from parser.parser import parse, SyntaxError
from parser.ast import *
from sys import argv

def _eval(expr: Expr, env: dict[str, int]) -> int:
    """Evaluate an expression."""
    if isinstance(expr, Int):
        return expr.value
    elif isinstance(expr, Id):
        if expr.id not in env:
            raise NameError(f"NameError: Name '{expr.id}' is not defined.")
        return env[expr.id]
    elif isinstance(expr, BinOp):
        left = _eval(expr.left, env)
        right = _eval(expr.right, env)
        if expr.op == "+":
            return left + right
        elif expr.op == "-":
            return left - right
        elif expr.op == "*":
            return left * right
        elif expr.op == "/":
            return left // right
        else:
            raise ValueError(f"Unknown op: {expr.op}")
    elif isinstance(expr, UnaryOp):
        if expr.op == "+":
            return _eval(expr.expr, env)
        elif expr.op == "-":
            return -_eval(expr.expr, env)
        else:
            raise ValueError(f"Unknown op: {expr.op}")
    else:
        raise TypeError(f"Unknown type: {type(expr)}")


def _assign(assign: Assign, env: dict[str, int]) -> tuple[str, int]:
    """Execute an assignment statement."""
    env[assign.id.id] = _eval(assign.expr, env)
    return assign.id.id, env[assign.id.id]


def _interpret(ast: AST) -> dict[str, int]:
    """Interpret an AST."""
    env = {}
    for statement in ast.statements:
        _assign(statement, env)
    return env


def run(prog: str) -> dict[str, int]:
    """Run a program."""
    return _interpret(parse(Lexer(prog)))


def repl() -> None:
    """Run the REPL."""
    env = {}
    last_line = ""
    print("Calc REPL: type '!q' to quit, Type '!h' for help.")
    while True:
        line = input(">>> ")
        if line == "!q":
            break
        if line == "!h":
            print("type !q to quit, !h for help")
        if line.startswith("!"):
            print("Unknown command")
        if line == "":
            line = last_line

        try:
            ast = parse(Lexer(line))
            if ast.statements:
                id, val = _assign(ast.statements[0], env)
            print(f"{id} = {val}")
        except (NameError, SyntaxError, LexerError) as e:
            print(e)
        
        last_line = line
    

def main() -> None:
    if len(argv) == 2:
        with open(argv[1]) as f:
            prog = f.read()
        
        try:
            print(run(prog))
        except (NameError, LexerError, SyntaxError) as e:
            print(e)
    else:
        repl()


if __name__ == "__main__":
    main()