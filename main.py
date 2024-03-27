"""Script for taking derivative of a function"""
import sys
import argparse
from functions.function import Function

sys.tracebacklimit = 0


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
        description="Script for taking derivative of a function")
    _ = parser.parse_args()

    function = Function("cbrt(x^2)")
    print(diff(function, x=0.0000000000000000000000000000001))


if __name__ == '__main__':
    main()
