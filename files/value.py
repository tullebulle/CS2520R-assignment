
# Base class for values
class Value:
    """Base class for all values in the interpreter."""
    pass

class BoolValue(Value):
    """Boolean values."""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "true" if self.value else "false"

class IntValue(Value):
    """Integer values."""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)

class Closure(Value):
    """A closure represents a lambda abstraction with an environment."""
    def __init__(self, param_name, param_type, body, env):
        self.param_name = param_name  # The parameter (a variable)
        self.param_type = param_type  # The parameter (a variable)
        self.body = body    # The body of the function (an expression)
        self.env = env      # The environment in which the function was created
    
    def __repr__(self):
            return f"<closure λ{self.param_name}: {self.param_type}. {self.body}>"
    

class PairValue(Value):
    """Represents an evaluated value of a pair (A ∧ B)."""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"PairValue({self.left}, {self.right})"
    
class InlValue(Value):
    """Represents the left injection value of a disjunction (A ∨ B)."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"InlValue({self.value})"


class InrValue(Value):
    """Represents the right injection value of a disjunction (A ∨ B)."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"InrValue({self.value})"

