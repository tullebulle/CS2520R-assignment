from .types import *

class TrueType(Type):
    """Represents the logical constant True."""
    def __repr__(self):
        return "True"

class FalseType(Type):
    """Represents the logical constant False."""
    def __repr__(self):
        return "False"

class AndType(Type):
    """Represents a conjunction type (A ∧ B)."""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

    def __eq__(self, other):
        return isinstance(other, AndType) and self.left == other.left and self.right == other.right

class OrType(Type):
    """Represents a disjunction type (A ∨ B)."""
    def __init__(self, left_type, right_type):
        if not isinstance(left_type, Type) or not isinstance(right_type, Type):
            raise TypeError(f"OrType expects types as arguments, but got {type(left_type), type(right_type)}")
        self.left = left_type # left type
        self.right = right_type # right type

    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

    def __eq__(self, other):
        return isinstance(other, OrType) and self.left == other.left and self.right == other.right
