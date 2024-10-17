# Define a class hierarchy for the expressions
class Expr:
    """Base class for all expressions."""
    pass

class Var(Expr):
    """A variable."""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name

class Abs(Expr):
    """A lambda abstraction (λx: T. E)."""
    def __init__(self, param_name, param_type, body):
        self.param_name = param_name  # The parameter name as a string
        self.param_type = param_type  # The type of the parameter
        self.body = body              # The body of the function
    
    def __repr__(self):
        return f"(λ {self.param_name}: {self.param_type}. {self.body})"

class App(Expr):
    """A function application (E1 E2)."""
    def __init__(self, func, arg):
        self.func = func  # The function being applied
        self.arg = arg    # The argument being applied to the function
    
    def __repr__(self):
        return f"({self.func} {self.arg})"
