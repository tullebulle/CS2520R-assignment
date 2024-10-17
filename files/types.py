# Base class for types
class Type:
    """Base class for types."""
    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.__class__)

class BoolType(Type):
    """Boolean type."""
    def __repr__(self):
        return "Bool"
    
    def __eq__(self, other):
        return isinstance(other, BoolType)

class IntType(Type):
    """Integer type."""
    def __repr__(self):
        return "Int"
    
    def __eq__(self, other):
        return isinstance(other, IntType)

class FuncType(Type):
    """Function type: A -> B."""
    def __init__(self, param_type, return_type):
        self.param_type = param_type  # Type of the function's parameter
        self.return_type = return_type  # Type of the function's return value
    
    def __repr__(self):
        return f"({self.param_type} -> {self.return_type})"

    def __eq__(self, other):
        # Two function types are equal if both their parameter and return types are equal
        return (isinstance(other, FuncType) and 
                self.param_type == other.param_type and 
                self.return_type == other.return_type)

    def __hash__(self):
        return hash((self.param_type, self.return_type))
