from .expressions import *
from .typechecker import *

class Inl(Expr):
    """Represents the left injection (A ∨ B) where the value is of type A."""
    def __init__(self, value, disjunction_type):
        """
        Initialize the left injection.
        
        Parameters:
        - value: The value of type A to be injected into the disjunction.
        - disjunction_type: An instance of OrType representing the entire disjunction (A ∨ B).
        """

        self.value = value
        self.typ = disjunction_type  # This should be an instance of OrType
        

    def __repr__(self):
        return f"inl({self.value})"


class Inr(Expr):
    """Represents the right injection (A ∨ B) where the value is of type B."""
    def __init__(self, value, disjunction_type):
        """
        Initialize the right injection.
        
        Parameters:
        - value: The value of type B to be injected into the disjunction.        """
        self.value = value
        self.typ = disjunction_type  # This should be an instance of OrType

    def __repr__(self):
        return f"inr({self.value})"


class Case(Expr):
    """Represents a case expression (for A ∨ B)."""
    def __init__(self, expr, left_case, right_case):
        self.expr = expr          # The disjunction expression
        self.left_case = left_case  # Case for the left type
        self.right_case = right_case  # Case for the right type

    def __repr__(self):
        return f"case {self.expr} of ({self.left_case}, {self.right_case})"
