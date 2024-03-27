"""Module that performs some methods defined in a function module"""
import argparse
from .function import Function


def diff(function: Function, variable: str = 'x', **values: dict) -> Function | float:
    """
    Function that takes a derivative of a given function

    Args:
        function (Function): Function to derive
        variable (str, optional): The variable of differentiation. Defaults to 'x'.
        **values: Positional arguments for function variables.\
            If specified calculates derivative at a given point

    Returns:
        Function | float: Derivative of a function
    """
    if values:
        return function.derive(variable, **values)
    return function.diff(variable)


def main() -> None:
    """
    Prints derivative of a specific function
    """
    parser = argparse.ArgumentParser(
        prog="derivative",
        description="Python package with tools for working with mathematical functions,\
            the main one of which is taking derivative")
    _ = parser.parse_args()

    function = Function("cbrt(x^2)")
    print(diff(function, x=0.00000000000000000000000001))


if __name__ == '__main__':
    main()
