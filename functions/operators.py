"""Operator describing module"""
from enum import Enum
import math


class OperatorType(Enum):
    """
    Enum class to describe operator type
    """
    BINARY = 0
    PREFIX = 1
    POSTFIX = 2


class Associativity(Enum):
    """
    Enum class to describe operator associativity
    """
    NONE = 0
    ASSOCIATIVE = 1
    LEFT_ASSOCIATIVE = 2
    RIGHT_ASSOCIATIVE = 3


class Operator:
    """
    Class for operators

    Args:
        operator_type (OperatorType): Operator type
        associativity (Associativity): Operator associativity
        priority (int): Operator priority
        func (callable): Corresponding operator function
    """

    def __init__(self, operator_type: OperatorType,
                 associativity: Associativity,
                 priority: int, func: callable) -> None:
        self._operator_type = operator_type
        self._associativity = associativity
        self._priority = priority
        self._function = func

    @property
    def operator_type(self) -> OperatorType:
        """
        Property that contains operator type

        Returns:
            OperatorType: Operator type
        """
        return self._operator_type

    @property
    def associativity(self) -> Associativity:
        """
        Property that contains operator associativity

        Returns:
            Associativity: Operator associativity
        """
        return self._associativity

    @property
    def priority(self) -> int:
        """
        Property that contains operator priority

        Returns:
            int: Operator priority
        """
        return self._priority

    def calculate(self, *args) -> float:
        """
        Method that calculates result of the operator with given arguments

        Args:
            *args: Arguments for the operator

        Returns:
            float: Result of the operator
        """
        return self._function(*args)


OPERATORS = {
    '+': Operator(OperatorType.BINARY, Associativity.ASSOCIATIVE,
                  0, lambda x, y: x + y),
    '-': Operator(OperatorType.BINARY, Associativity.LEFT_ASSOCIATIVE,
                  0, lambda x, y: x - y),
    'unary-': Operator(OperatorType.PREFIX, Associativity.NONE,
                       1, lambda x: -x),
    '*': Operator(OperatorType.BINARY, Associativity.ASSOCIATIVE,
                  1, lambda x, y: x * y),
    '/': Operator(OperatorType.BINARY, Associativity.LEFT_ASSOCIATIVE,
                  1, lambda x, y: x / y),
    '^': Operator(OperatorType.BINARY, Associativity.RIGHT_ASSOCIATIVE,
                  2, lambda x, y: x ** y),
    'sqrt': Operator(OperatorType.PREFIX, Associativity.NONE,
                     3, math.sqrt),
    'exp': Operator(OperatorType.PREFIX, Associativity.NONE,
                    3, math.exp),
    'ln': Operator(OperatorType.PREFIX, Associativity.NONE,
                   3, math.log),
    'sin': Operator(OperatorType.PREFIX, Associativity.NONE,
                    3, math.sin),
    'cos': Operator(OperatorType.PREFIX, Associativity.NONE,
                    3, math.cos),
    'tg': Operator(OperatorType.PREFIX, Associativity.NONE,
                   3, math.tan),
}

CONSTANTS = {
    'e': math.e,
    'pi': math.pi,
    'tau': math.tau,
    'phi': (1 + math.sqrt(5)) / 2,
}
