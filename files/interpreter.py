# Environment to map variables to their values
from .expressions import *
from .value import *
from .ifcondition import *
from .binop import *
from .typechecker import *

class Env:
    def __init__(self, parent=None):
        self.env = {} #key is str and value is value
        self.parent = parent  # For nested environments (closures)

    def extend(self, var, value):
        """Extend the current environment with a new variable binding."""
        self.env[var] = value

    def lookup(self, var):
        """Look up the value of a variable in the current or parent environment."""
        if var in self.env:
            return self.env[var]
        elif self.parent:
            return self.parent.lookup(var)
        else:
            raise NameError(f"Variable '{var}' is not instantiated in the environment")


# Interpreter function
def eval_expr(expr, env):
    """Evaluate an expression in a given environment."""
    
    if isinstance(expr, Var):
        return env.lookup(expr.name)

    elif isinstance(expr, Abs):
        return Closure(expr.param_name, expr.param_type, expr.body, env)

    elif isinstance(expr, App):
        func = eval_expr(expr.func, env)
        arg = eval_expr(expr.arg, env)

        if isinstance(func, Abs):
            func = eval_expr(func, env)

        if isinstance(func, Closure):
            extended_env = Env(func.env)
            extended_env.extend(func.param_name, arg)
            return eval_expr(func.body, extended_env)
        else:
            raise TypeError(f"Expected a function, but got {func}")

    elif isinstance(expr, IntValue):
        return expr

    elif isinstance(expr, BoolValue):
        return expr

    elif isinstance(expr, Pair):
        # Evaluate both components of the pair
        left_value = eval_expr(expr.left, env)
        right_value = eval_expr(expr.right, env)
        return Pair(left_value, right_value)

    elif isinstance(expr, Fst):
        # Evaluate the pair and extract the first element
        pair_value = eval_expr(expr.pair, env)
        if isinstance(pair_value, Pair):
            return pair_value.left
        else:
            raise TypeError("fst can only be applied to a pair.")

    elif isinstance(expr, Snd):
        # Evaluate the pair and extract the second element
        pair_value = eval_expr(expr.pair, env)
        if isinstance(pair_value, Pair):
            return pair_value.right
        else:
            raise TypeError("snd can only be applied to a pair.")

    elif isinstance(expr, Inl):
        # Evaluate the value and wrap it in Inl
        value = eval_expr(expr.value, env)
        return InlValue(value)

    elif isinstance(expr, Inr):
        # Evaluate the value and wrap it in Inr
        value = eval_expr(expr.value, env)
        return InrValue(value)

    elif isinstance(expr, Case):
        disjunction_value = eval_expr(expr.expr, env)

        if isinstance(disjunction_value, InlValue):
            # Extend environment with the variable bound to the left value
            extended_env = Env(env)
            extended_env.extend('a', disjunction_value)
            return eval_expr(expr.left_case, extended_env)

        elif isinstance(disjunction_value, InrValue):
            # Extend environment with the variable bound to the right value
            extended_env = Env(env)
            extended_env.extend('b', disjunction_value)
            return eval_expr(expr.right_case, extended_env)

        else:
            raise TypeError("Expected a disjunction (Inl or Inr).")

    elif isinstance(expr, If):
        condition_value = eval_expr(expr.condition, env)

        if not isinstance(condition_value, BoolValue):
            raise TypeError(f"Condition must evaluate to a Bool, but got {condition_value}")

        if condition_value.value:
            return eval_expr(expr.then_branch, env)
        else:
            return eval_expr(expr.else_branch, env)

    elif isinstance(expr, BinOp):
        left_value = eval_expr(expr.left, env)
        right_value = eval_expr(expr.right, env)

        if expr.op in ['+', '-', '*', '/']:
            if isinstance(left_value, IntValue) and isinstance(right_value, IntValue):
                if expr.op == '+':
                    return IntValue(left_value.value + right_value.value)
                elif expr.op == '-':
                    return IntValue(left_value.value - right_value.value)
                elif expr.op == '*':
                    return IntValue(left_value.value * right_value.value)
                elif expr.op == '/':
                    if right_value.value == 0:
                        raise ZeroDivisionError("Division by zero")
                    return IntValue(left_value.value // right_value.value)

        elif expr.op in ['&&', '||']:
            if isinstance(left_value, BoolValue) and isinstance(right_value, BoolValue):
                if expr.op == '&&':
                    return BoolValue(left_value.value and right_value.value)
                elif expr.op == '||':
                    return BoolValue(left_value.value or right_value.value)

        elif expr.op in ['==', '<', '>']:
            if isinstance(left_value, IntValue) and isinstance(right_value, IntValue):
                if expr.op == '==':
                    return BoolValue(left_value.value == right_value.value)
                elif expr.op == '<':
                    return BoolValue(left_value.value < right_value.value)
                elif expr.op == '>':
                    return BoolValue(left_value.value > right_value.value)

        raise TypeError(f"Invalid operands for binary operation: {expr.op}")

    else:
        raise TypeError(f"Unknown expression type: {expr}")
