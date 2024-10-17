from .expressions import *

class If(Expr):
    """Represents an if-then-else expression."""
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def __repr__(self):
        return f"(if {self.condition} then {self.then_branch} else {self.else_branch})"
