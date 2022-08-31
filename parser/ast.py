"""
    An ast representing the calc program.
"""


class AST:
    pass


class Expr(AST):
    pass


class Int(Expr):
    def __init__(self, value: int) -> None:
        self.value = value


class Id(Expr):
    def __init__(self, id: str) -> None:
        self.id = id


class BinOp(Expr):
    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(Expr):
    def __init__(self, op: str, expr: Expr) -> None:
        self.op = op
        self.expr = expr


class Assign(AST):
    def __init__(self, id: Id, expr: Expr):
        self.id = id
        self.expr = expr


class Program(AST):
    def __init__(self, statements: list[Assign]) -> None:
        self.statements = statements