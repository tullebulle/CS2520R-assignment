from .expressions import *
from .types import *
from .value import *
from .ifcondition import *
from .binop import *
from .conjuntiontypes import *
from .disjunctions import *
from .logicaltypes import *

# Type context to map variables to types
class TypeContext:
    def __init__(self):
        self.context = {}

    def add(self, var, typ):
        """Add a variable with its type to the context."""
        if not isinstance(typ, Type):
            raise TypeError(f"Second argument must be of type Type, got type {type(typ)}")
        self.context[var] = typ

    def lookup(self, var):
        """Return the type of a variable, or raise an error if it's not found."""
        if var not in self.context:
            raise TypeError(f"Variable {var} not found in context")
        return self.context[var]

# Type checker function
def type_check(expr, context):
    """Recursively type-check an expression given a type context."""
    

    if isinstance(expr, Pair):
        left_type = type_check(expr.left, context)
        right_type = type_check(expr.right, context)
        return AndType(left_type, right_type)

    elif isinstance(expr, Fst):
        pair_type = type_check(expr.pair, context)
        if isinstance(pair_type, AndType):
            return pair_type.left
        else:
            raise TypeError("fst can only be applied to a conjunction (A ∧ B).")

    elif isinstance(expr, Snd):
        pair_type = type_check(expr.pair, context)
        if isinstance(pair_type, AndType):
            return pair_type.right
        else:
            raise TypeError("snd can only be applied to a conjunction (A ∧ B).")

    if isinstance(expr, Inl):
        value_type = type_check(expr.value, context)
        if isinstance(expr.typ, OrType) and value_type == expr.typ.left:
            return expr.typ
        else:
            raise TypeError("The value for inl must match the left type of the disjunction.")

    elif isinstance(expr, Inr):
        value_type = type_check(expr.value, context)
        if isinstance(expr.typ, OrType) and value_type == expr.typ.right:
            return expr.typ
        else:
            raise TypeError("The value for inr must match the right type of the disjunction.")

    if isinstance(expr, Case):
        disjunction_type = type_check(expr.expr, context)

        if isinstance(disjunction_type, OrType):
            context.add('a', disjunction_type.left)

            context.add('b', disjunction_type.right)

            left_type = type_check(expr.left_case, context)
            right_type = type_check(expr.right_case, context)

            if left_type == right_type:
                return left_type
            else:
                raise TypeError("Both branches of the case expression must return the same type.")
        else:
            raise TypeError("Case expression must be applied to a disjunction (A ∨ B).")
    
    elif isinstance(expr, Var):
        # Look up the type of the variable in the context
        return context.lookup(expr.name)
    

    elif isinstance(expr, Abs):
        # Add the parameter type to the context using the parameter name
        context.add(expr.param_name, expr.param_type)

        # Type-check the body
        body_type = type_check(expr.body, context)

        # Remove the parameter from the context after type-checking the body
        context.context.pop(expr.param_name, None)

        return FuncType(expr.param_type, body_type)

    elif isinstance(expr, App):
        # For an application (E1 E2), check that E1 is a function and E2 matches its argument type
        func_type = type_check(expr.func, context)
        arg_type = type_check(expr.arg, context)

        if isinstance(func_type, FuncType):
            if func_type.param_type == arg_type:
                return func_type.return_type
            elif isinstance(func_type.param_type, OrType):
                return func_type.return_type
            else:
                raise TypeError(f"Type mismatch: expected {func_type.param_type} but got {arg_type}")
        else:
            raise TypeError(f"Expected a function, but got {func_type}")
        
    # elif isinstance(expr, PairValue):
    #     return PairValue(type_check(expr.left, context), type_check(expr.right, context))

    elif isinstance(expr, IntValue):
        # Return IntType when evaluating an integer value
        return IntType()

    elif isinstance(expr, BoolValue):
        # Return BoolType when evaluating a boolean value
        return BoolType()
    
    elif isinstance(expr, If):
        # Type-check the condition
        condition_type = type_check(expr.condition, context)
        if condition_type != BoolType():
            raise TypeError(f"Condition in if must be Bool, but got {condition_type}")

        # Type-check the then and else branches
        then_type = type_check(expr.then_branch, context)
        else_type = type_check(expr.else_branch, context)

        if then_type != else_type:
            raise TypeError(f"Type mismatch in branches: {then_type} vs {else_type}")

        return then_type
    
    elif isinstance(expr, BinOp):
        left_type = type_check(expr.left, context)
        right_type = type_check(expr.right, context)
        
        if expr.op in ['+', '-', '*', '/']:
            if left_type == IntType() and right_type == IntType():
                return IntType()
            else:
                raise TypeError(f"Arithmetic operations require Int types, but got {left_type} and {right_type}")

        elif expr.op in ['&&', '||']:
            if left_type == BoolType() and right_type == BoolType():
                return BoolType()
            else:
                raise TypeError(f"Boolean operations require Bool types, but got {left_type} and {right_type}")

        elif expr.op in ['==', '<', '>']:
            if left_type == IntType() and right_type == IntType():
                return BoolType()
            else:
                raise TypeError(f"Comparison operations require Int types, but got {left_type} and {right_type}")

        else:
            raise TypeError(f"Unknown binary operation: {expr.op}")

    else:
        raise TypeError(f"Unknown expression type: {expr}")
