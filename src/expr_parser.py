"""Module that provides functionality for parsing mathematical expressions"""
import re
from operators import OPERATORS, CONSTANTS, OperatorType, Associativity

NUM_REGEX = re.compile(r"[\d,.]+")
VAR_REGEX = re.compile(r"[A-Za-z]+")


class ParserException(Exception):
    """
    Base exception for errors that may occur during expression parsing

    Args:
        expression (str): Expression that is being parsed
        position (int): Position in the expression where the problem occurred
        length (int): Length of the token in the expression which caused a problem
    """

    def __init__(self, expression: str, position: int, length: int, *args: object) -> None:
        super().__init__(*args)
        self.expression = expression
        self.position = position
        self.length = length

    def __str__(self):
        return f"\n{self.expression}\n{'^' * self.length: >{self.position + self.length}}"


class ParenthesisMismatchError(ParserException):
    """
    Raises when an expression contains wrong placement of parenthesis

    Args:
        expression (str): The expression that is being parsed
        position (int): Position in the expression where the parenthesis mismatch error occured
    """

    def __init__(self, expression: str, position: int, *args: object) -> None:
        super().__init__(expression, position, 1, *args)


class InvalidCharacterError(ParserException):
    """
    Raises when an expression contains invalid characters

    Args:
        expression (str): The expression that is being parsed
        position (int): Position in the expression where the invalid character was found
    """

    def __init__(self, expression: str, position: int, *args: object) -> None:
        super().__init__(expression, position, 1, *args)


class EntitiesPlacementError(ParserException):
    """
    Raises when an expression contains incorrect placement of operands or operators

    Args:
        expression (str): The expression that is being parsed
        position (int): Position in the expression where the placement error occurred
        length (int): Length of the incorrectly placed entity
    """


class InvalidNumberError(ParserException):
    """
    Raises when an expression contains invalid numbers

    Args:
        expression (str): The expression that is being parsed
        position (int): Position in the expression where the invalid number was found
        length (int): Length of the invalid number
    """


class Parser:
    """
    Class with methods to parse a mathematical expression

    Args:
        expression (str): The expression to parse
    """

    def __init__(self, expression: str) -> None:
        self._expression = "".join(expression.split())
        self._rpn = None

    @property
    def expression(self) -> str:
        """
        Property that contains original expression

        Returns:
            str: The original mathematical expression
        """
        return self._expression

    @property
    def rpn(self) -> list:
        """
        Property that contains given expression in reverse polish notation

        Returns:
            list: A list of expression tokens written in reverse polish notation
        """
        if self._rpn is None:
            self._rpn = self._parse_to_rpn()
        return self._rpn

    def _parse_to_rpn(self) -> list:
        stack = []
        result = []
        tokens = self._tokenize()
        prev_token = None
        position = 0
        open_bracket_pos = []

        def add_binary_op(operator: str) -> None:
            nonlocal stack, result, peek
            while stack and peek in OPERATORS and \
                (OPERATORS.get(peek).priority > OPERATORS.get(operator).priority or
                 (OPERATORS.get(peek).associativity != Associativity.RIGHT_ASSOCIATIVE and
                  OPERATORS.get(peek).priority == OPERATORS.get(operator).priority)):
                result.append(stack.pop())
                peek = self._peek(stack)
            stack.append(operator)

        def add_skipped_mul() -> None:
            nonlocal prev_token
            prev_op_type = getattr(OPERATORS.get(
                prev_token), 'operator_type', None)
            if (prev_token is not None and prev_token not in OPERATORS and prev_token != '(') or \
                    prev_op_type == OperatorType.POSTFIX:
                add_binary_op('*')

        for token in tokens:
            peek = self._peek(stack)

            if token in OPERATORS:
                if token == '-' and (prev_token is None or
                                     prev_token == '(' or
                                     prev_token in OPERATORS):
                    token = 'unary-'
                if OPERATORS.get(token).operator_type == OperatorType.POSTFIX:
                    self._entity_placement_error_checker(prev_token, position,
                                                         len(token), False)
                    result.append(token)
                elif OPERATORS.get(token).operator_type == OperatorType.PREFIX:
                    add_skipped_mul()
                    stack.append(token)
                elif OPERATORS.get(token).operator_type == OperatorType.BINARY:
                    self._entity_placement_error_checker(prev_token, position,
                                                         len(token), False)
                    add_binary_op(token)

            elif token == '(':
                add_skipped_mul()
                open_bracket_pos.append(position)
                stack.append(token)

            elif token == ')':
                self._entity_placement_error_checker(
                    prev_token, position, 1, False)
                while stack and peek != '(':
                    result.append(stack.pop())
                    peek = self._peek(stack)
                if stack:
                    peek = self._peek(stack)
                    stack.pop()
                self._parenthesis_mismatch_error_checker(peek, position,
                                                         None, False)
                open_bracket_pos.pop()

            else:
                self._invalid_number_error_checker(token, position)
                add_skipped_mul()
                result.append(token)

            prev_token = token
            position += len(token) if token != 'unary-' else 1

        if position:
            position -= len(prev_token)
            self._entity_placement_error_checker(prev_token, position,
                                                 len(prev_token), True)

        while stack:
            entity = stack.pop()
            self._parenthesis_mismatch_error_checker(entity, None,
                                                     open_bracket_pos, True)
            result.append(entity)

        return result

    def _tokenize(self) -> list:
        result = []
        temp = ""
        position = 0

        def add_num_to_tokens():
            nonlocal result, temp
            if NUM_REGEX.match(temp):
                temp = temp.replace(',', '.')
                result.append(temp)
                temp = ""

        def add_var_to_tokens():
            nonlocal result, temp
            if VAR_REGEX.match(temp):
                result += list(temp)
                temp = ""

        for index, char in enumerate(self.expression):
            if char in OPERATORS or char in ['(', ')']:
                add_num_to_tokens()
                add_var_to_tokens()
                result.append(char)
            elif NUM_REGEX.match(char):
                add_var_to_tokens()
                temp += char
            elif VAR_REGEX.match(char):
                add_num_to_tokens()
                temp += char
                for symbol in OPERATORS | CONSTANTS:
                    if char == 'e' and self.expression[index:index + 3] == 'exp':
                        break
                    if temp.endswith(symbol):
                        result += list(temp[:-len(symbol)])
                        result.append(symbol)
                        temp = ""
            else:
                raise InvalidCharacterError(self.expression, position)
            position += 1

        if temp:
            add_num_to_tokens()
            add_var_to_tokens()
        return result

    def _peek(self, stack):
        return stack[-1] if stack else None

    def _entity_placement_error_checker(self, token, position: int,
                                        length: int, last: bool) -> None:
        if ((token in OPERATORS and OPERATORS[token].operator_type
                in (OperatorType.BINARY, OperatorType.PREFIX)) or token == '(' or
                token is None) and not last:
            raise EntitiesPlacementError(self.expression, position, length)
        if (token in OPERATORS and OPERATORS[token].operator_type
                in (OperatorType.BINARY, OperatorType.PREFIX)) and last:
            raise EntitiesPlacementError(self.expression, position, length)

    def _parenthesis_mismatch_error_checker(self, token, position: int,
                                            open_bracket_pos: list, last: bool) -> None:
        if not last and token != '(':
            raise ParenthesisMismatchError(self.expression, position)
        if last and token == '(':
            raise ParenthesisMismatchError(self.expression,
                                           open_bracket_pos.pop())

    def _invalid_number_error_checker(self, token, position: int) -> None:
        if NUM_REGEX.match(token):
            try:
                float(token)
            except ValueError as exc:
                raise InvalidNumberError(self.expression,
                                         position, len(token)) from exc


a = Parser("xyz")
print(a.rpn)
