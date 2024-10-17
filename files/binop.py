from .expressions import *

class BinOp(Expr):
    """Represents a binary operation (e.g., x + y)."""
    def __init__(self, left, op, right):
        self.left = left   # The left operand
        self.op = op       # The operation ('+', '-', '*', '/', '&&', '||', '==', '<', '>')
        self.right = right # The right operand
    
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"
