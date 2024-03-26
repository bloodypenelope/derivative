"""Module that provides functionality for working with mathematical functions"""
from sympy import sympify, simplify, nsimplify
from operators import OPERATORS, CONSTANTS, OperatorType, Associativity
from expr_parser import Parser, NUM_REGEX


class Function:
    """
    Class that represents a mathematical function

    Args:
        expression (str, optional): The mathematical expression that represents a function.\
            Defaults to None
    """

    def __init__(self, expression: str = None) -> None:
        self.left = None
        self.right = None
        self.value = None

        if expression:
            rpn = Parser(expression).rpn
            self.build_tree(rpn)

    def build_tree(self, rpn: list) -> None:
        """
        Method that builds AVL-tree of an expression based on its RPN form

        Args:
            rpn (list): RPN of an expression represented as a list of tokens
        """
        if not rpn:
            return

        token = rpn.pop()
        if NUM_REGEX.match(token):
            self.value = float(token)
        else:
            self.value = token

        if token not in OPERATORS:
            return

        if OPERATORS[token].operator_type == OperatorType.BINARY:
            self.right = Function()
            self.right.build_tree(rpn)

        self.left = Function()
        self.left.build_tree(rpn)

    def validate_function(self, **values) -> bool:
        """
        Method checks if function has an illegal operation (e.g. division by zero)

        Args:
            **values: Positional arguments for function variables. \
                Can be specified to check if function is valide at certain point

        Returns:
            bool: Function validity
        """
        try:
            self.calculate(**values)
        except (ZeroDivisionError, ValueError):
            return False
        return True

    def simplify(self):
        """
        Method that simplifies and returns new function

        Returns:
            Function: Simplified function
        """
        if not self.validate_function():
            return self
        expr = str(self).replace('tg', 'tan').replace('e', 'E')
        simplified = str(simplify(nsimplify(sympify(expr))))
        simplified = simplified.replace('tan', 'tg') \
            .replace('E', 'e').replace('log', 'ln').replace('**', '^')
        return Function(simplified)

    def calculate(self, **values: dict):
        """
        Method that evaluates a function with given variables

        Args:
            **values: Positional arguments for function variables.\
                Not necessary to include all or any of them

        Raises:
            ZeroDivisionError: Raises when division by zero occurs
            ValueError: Raises when a function receives an argument that is out of its domain

        Returns:
            Function: Reduced function with the calculations performed
        """
        result = Function()
        if self.value in values:
            result.value = values[self.value]
            return result
        if self.value in CONSTANTS:
            result.value = CONSTANTS[self.value]
            return result

        result.value = self.value
        if result.value not in OPERATORS:
            return result

        result.left = self.left.calculate(**values)
        if OPERATORS[result.value].operator_type == OperatorType.BINARY:
            result.right = self.right.calculate(**values)
            if result.value == '/' and result.right.value == 0.0:
                raise ZeroDivisionError

            if isinstance(result.left.value, (int, float)) and \
                    isinstance(result.right.value, (int, float)):
                if result.value == '^' and result.left.value == 0.0 and result.right.value <= 0:
                    raise ZeroDivisionError
                value = OPERATORS[result.value].calculate(
                    result.left.value, result.right.value)
                if isinstance(value, complex):
                    raise ValueError("Argument is out of function domain")
                result.value = value
                result.left = result.right = None
        elif isinstance(result.left.value, (int, float)):
            if result.value == 'sqrt' and result.left.value < 0.0:
                raise ValueError("Argument is out of function domain")
            if result.value == 'ln' and result.left.value <= 0.0:
                raise ValueError("Argument is out of function domain")

            value = OPERATORS[result.value].calculate(result.left.value)
            result.value = value
            result.left = None
        return result

    def derive(self, variable: str = 'x', **values: dict) -> float:
        """
        Method that takes derivative of a function\
            with respect to a given variable and at a given point

        Args:
            variable (str, optional): The variable of differentiation. Defaults to 'x'
            **values: Positional arguments for function variables.

        Raises:
            ValueError: Raises when either a given point is specified incorrectly\
                or when a derivative does not exists at that point

        Returns:
            float: Derivative of a function at a given point
        """
        derivative = self.diff(variable)
        if self.validate_function(**values) and derivative.validate_function(**values):
            value = derivative.calculate(**values).value
            if not isinstance(value, (int, float)):
                raise ValueError("Point was not specified correctly")
            return value
        raise ValueError("Derivative at that point does not exist")

    def diff(self, variable: str = 'x'):
        """
        Method that differentiates a function

        Args:
            variable (str, optional): The variable of differentiation. Defaults to 'x'

        Returns:
            Function: Derivative of a function
        """
        if self.value is None:
            return Function()

        derivative = None
        match self.value:
            case '+':
                derivative = self._diff_sum(variable)
            case '-':
                derivative = self._diff_sum(variable)
            case 'unary-':
                derivative = self._diff_unary_min(variable)
            case '*':
                derivative = self._diff_prod(variable)
            case '/':
                derivative = self._diff_div(variable)
            case '^':
                derivative = self._diff_pow(variable)
            case 'sqrt':
                derivative = self._diff_sqrt(variable)
            case 'cbrt':
                derivative = self._diff_cbrt(variable)
            case 'exp':
                derivative = self._diff_exp(variable)
            case 'ln':
                derivative = self._diff_ln(variable)
            case 'sin':
                derivative = self._diff_sin(variable)
            case 'cos':
                derivative = self._diff_cos(variable)
            case 'tg':
                derivative = self._diff_tg(variable)
            case _: derivative = self._diff_var(variable)
        return derivative.simplify()

    def _diff_sum(self, variable: str):
        derivative = Function()
        derivative.value = self.value
        derivative.left = self.left.diff(variable)
        derivative.right = self.right.diff(variable)
        return derivative

    def _diff_unary_min(self, variable: str):
        derivative = Function()
        derivative.value = self.value
        derivative.left = self.left.diff(variable)
        return derivative

    def _diff_prod(self, variable: str):
        derivative = Function()
        derivative.value = '+'

        derivative.left = Function()
        derivative.left.value = '*'
        derivative.left.left = self.left.diff(variable)
        derivative.left.right = self.right

        derivative.right = Function()
        derivative.right.value = '*'
        derivative.right.left = self.left
        derivative.right.right = self.right.diff(variable)
        return derivative

    def _diff_div(self, variable: str):
        derivative = Function()
        derivative.value = '/'

        derivative.left = Function()
        derivative.left.value = '-'

        derivative.left.left = Function()
        derivative.left.left.value = '*'
        derivative.left.left.left = self.left.diff(variable)
        derivative.left.left.right = self.right

        derivative.left.right = Function()
        derivative.left.right.value = '*'
        derivative.left.right.left = self.left
        derivative.left.right.right = self.right.diff(variable)

        derivative.right = Function()
        derivative.right.value = '^'

        derivative.right.left = self.right

        derivative.right.right = Function()
        derivative.right.right.value = 2.0
        return derivative

    def _diff_pow(self, variable: str):
        derivative = Function()
        derivative.value = '*'

        derivative.left = Function()
        derivative.left.value = '+'

        derivative.left.left = Function()
        derivative.left.left.value = '/'

        derivative.left.left.left = Function()
        derivative.left.left.left.value = '*'

        derivative.left.left.left.left = self.left.diff(variable)
        derivative.left.left.left.right = self.right

        derivative.left.left.right = self.left

        derivative.left.right = Function()
        derivative.left.right.value = '*'

        derivative.left.right.left = Function()
        derivative.left.right.left.value = 'ln'

        derivative.left.right.left.left = self.left

        derivative.left.right.right = self.right.diff(variable)

        derivative.right = Function()
        derivative.right.value = '^'

        derivative.right.left = self.left
        derivative.right.right = self.right
        return derivative

    def _diff_sqrt(self, variable: str):
        derivative = Function()
        derivative.value = '/'

        derivative.left = self.left.diff(variable)

        derivative.right = Function()
        derivative.right.value = '*'

        derivative.right.left = Function()
        derivative.right.left.value = 2.0

        derivative.right.right = Function()
        derivative.right.right.value = 'sqrt'
        derivative.right.right.left = self.left
        return derivative

    def _diff_cbrt(self, variable: str):
        derivative = Function()
        derivative.value = '/'

        derivative.left = self.left.diff(variable)

        derivative.right = Function()
        derivative.right.value = '*'

        derivative.right.left = Function()
        derivative.right.left.value = 3.0

        derivative.right.right = Function()
        derivative.right.right.value = 'cbrt'

        derivative.right.right.left = Function()
        derivative.right.right.left.value = '^'
        derivative.right.right.left.left = self.left

        derivative.right.right.left.right = Function()
        derivative.right.right.left.right.value = 2.0
        return derivative

    def _diff_exp(self, variable: str):
        derivative = Function()
        derivative.value = '*'
        derivative.left = self.left.diff(variable)

        derivative.right = Function()
        derivative.right.value = 'exp'
        derivative.right.left = self.left
        return derivative

    def _diff_ln(self, variable: str):
        derivative = Function()
        derivative.value = '/'
        derivative.left = self.left.diff(variable)
        derivative.right = self.left
        return derivative

    def _diff_sin(self, variable: str):
        derivative = Function()
        derivative.value = '*'

        derivative.left = self.left.diff(variable)

        derivative.right = Function()
        derivative.right.value = 'cos'
        derivative.right.left = self.left
        return derivative

    def _diff_cos(self, variable: str):
        derivative = Function()
        derivative.value = 'unary-'

        derivative.left = Function()
        derivative.left.value = '*'

        derivative.left.left = self.left.diff(variable)

        derivative.left.right = Function()
        derivative.left.right.value = 'sin'
        derivative.left.right.left = self.left
        return derivative

    def _diff_tg(self, variable: str):
        derivative = Function()
        derivative.value = '/'
        derivative.left = self.left.diff(variable)

        derivative.right = Function()
        derivative.right.value = '^'

        derivative.right.left = Function()
        derivative.right.left.value = 'cos'
        derivative.right.left.left = self.left

        derivative.right.right = Function()
        derivative.right.right.value = 2.0
        return derivative

    def _diff_var(self, variable: str):
        derivative = Function()
        derivative.value = 1.0 if self.value == variable else 0.0
        return derivative

    def __str__(self) -> str:
        if self.value is None:
            return ""
        if not self.validate_function():
            return "undefined"
        tokens = []
        self.tokenize_tree(tokens)
        expr = "".join(map(str, tokens))
        return expr

    def tokenize_tree(self, tokens: list) -> None:
        """
        Method that tokenize an AVL-tree of a function and stores them in a given list

        Args:
            tokens (list): List for storing tokens of a function
        """
        if self.value not in OPERATORS:
            tokens.append(self.value)
            return

        if OPERATORS[self.value].operator_type == OperatorType.PREFIX:
            if self.value == 'unary-':
                tokens.append('-')
            else:
                tokens.append(self.value)
            self._tree_op_wrapper(self.left, tokens)
        else:
            self._tree_op_wrapper(self.left, tokens)
            tokens.append(self.value)

        if OPERATORS[self.value].operator_type == OperatorType.BINARY:
            self._tree_op_wrapper(self.right, tokens)

    def _tree_op_wrapper(self, child, tokens: list) -> None:
        wrap_child_operator = child.value in OPERATORS and \
            (OPERATORS[self.value].priority > OPERATORS[child.value].priority or
             (OPERATORS[self.value].priority == OPERATORS[child.value].priority and
              ((child == self.right and
                OPERATORS[self.value].associativity == Associativity.LEFT_ASSOCIATIVE) or
               (child == self.left and
                OPERATORS[self.value].associativity == Associativity.RIGHT_ASSOCIATIVE))))

        if OPERATORS[self.value].operator_type != OperatorType.BINARY or wrap_child_operator:
            tokens.append('(')
            child.tokenize_tree(tokens)
            tokens.append(')')
        else:
            child.tokenize_tree(tokens)
