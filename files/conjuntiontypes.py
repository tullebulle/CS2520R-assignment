from .expressions import *

class Pair(Expr):
    """Represents a pair (A ∧ B)."""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.right})"

class Fst(Expr):
    """Represents the first projection from a pair (fst)."""
    def __init__(self, pair):
        self.pair = pair

    def __repr__(self):
        return f"fst({self.pair})"

class Snd(Expr):
    """Represents the second projection from a pair (snd)."""
    def __init__(self, pair):
        self.pair = pair

    def __repr__(self):
        return f"snd({self.pair})"
