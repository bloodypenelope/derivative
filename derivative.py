"""Module for taking derivative of a function"""
import argparse
from functions.function import Function


def diff(function: str, variable: str = 'x', **values: dict) -> str:
    """
    Function that takes a derivative of a given mathematical function

    Args:
        function (str): Mathematical function to derive
        variable (str, optional): The variable of differentiation. Defaults to 'x'
        **values: Positional arguments for function variables.\
            If specified calculates derivative at a given point

    Returns:
        str: Derivative of a function
    """
    if values:
        return str(Function(function).derive(variable, **values))
    return str(Function(function).diff(variable))


def main() -> None:
    """
    Prints derivative of a specific function
    """
    parser = argparse.ArgumentParser(
        prog='derivative',
        description='Module with functionallity for differentiation mathematical functions.\
            (e.g. [derivative.diff("x^2") -> 2.0*x], [derivative.diff("x^2", x=2) -> 4.0])')
    _ = parser.parse_args()

    print(diff(diff(diff("x^3"))))


if __name__ == '__main__':
    main()
