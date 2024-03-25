from function import Function


def diff(function: Function, variable: str = 'x', **values: dict):
    if values:
        return function.derive(variable, **values)
    return function.diff(variable)


def main():
    function = Function("e^x.")
    print(diff(diff(diff(function))))


if __name__ == '__main__':
    main()
