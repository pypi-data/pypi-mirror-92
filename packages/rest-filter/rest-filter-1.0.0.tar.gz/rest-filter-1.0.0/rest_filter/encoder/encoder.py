from typing import List, ClassVar
import re

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node

from .base_types import Expression, BooleanOperation, BinaryOperation, Field


class Encoder(NodeVisitor):
    """
    This encoder enables you to encode a filtering string into a structured expression.
    """

    _base_peg_grammar = r"""
expression = "(" nspaces 
                 ( 
                     (field spaces ratio spaces value) /
                     (expression spaces binary_logical_operator spaces expression) 
                 ) 
             nspaces ")" 

# Values
string = "'" ~"[^']*"i "'"
# TODO: Write a smarter num regex to accept decimals & ignore -0, 00019
number = ~"-?\d+"i
true = "true"
false = "false"
boolean = true / false
value = string / number / boolean

# Spaces
spaces = " "+
nspaces = spaces?

# Fields
field = key ("\\" key)*
key = ~"[a-z]([a-z]|[0-9]|_)*"i&(" ")
# key = "age"

# Auto generated rules come here
"""

    # A map of ratio symbols to a BinaryOperation class
    registered_ratios = {}

    # A map of binary logical operator symbols to a BooleanOperation class
    registered_binary_logical_operators = {}

    def register_ratio(self, symbol: str):
        """
        Register a new type of ratio into the encoder.
        once the new ratio is registered, the encoder is able to detect that new ratio.

        The class being decorated must be a subclass of the BinaryOperation class
        :param symbol: The symbol that represents this ratio in the unencoded expression
        :return: A decorator for a ratio class
        """

        def register_decorator(cls: ClassVar):
            grammar_rule_name = f'registered_ratio_{cls.__name__}'
            self.registered_ratios[grammar_rule_name] = {
                'class': cls,
                'symbol': symbol
            }

            # Create the visitor func that returns the ration class
            visit_func_name = f'visit_{grammar_rule_name}'
            setattr(self, visit_func_name, lambda *args, **kwargs: cls)

            return cls

        return register_decorator

    def register_binary_logical_operator(self, symbol: str):
        """
        Register a new type of binary logical operator into the encoder.
        once the new operator is registered, the encoder is able to detect that new operator

        A binary logical operator is an operator that accepts two
        logical values / expressions representing boolean values and returns a single boolean value.

        The class being decorated must be a subclass of the BinaryOperation class
        :param symbol: The symbol that represents this operation in the unencoded expression
        :return: A decorator for a binary boolean operator class
        """

        def register_decorator(cls: ClassVar):
            grammar_rule_name = f'registered_binary_logical_operator_{cls.__name__}'
            self.registered_binary_logical_operators[grammar_rule_name] = {
                'class': cls,
                'symbol': symbol
            }

            # Create the visitor func that returns the operator class
            visit_func_name = f'visit_{grammar_rule_name}'
            setattr(self, visit_func_name, lambda *args, **kwargs: cls)

            return cls

        return register_decorator

    def _get_peg_format_grammar(self) -> str:
        """
        Generate and return the PEG grammar of the encoder
        :return: A multiline string of the encoders PEG grammar, including the registered objects
        """

        lines = self._base_peg_grammar.splitlines()

        # Add ratios to grammar
        lines.append('')
        lines.append('# Ratio rules')
        ratios_rule = f'ratio = {" / ".join(self.registered_ratios.keys())}'
        lines.append(ratios_rule)
        for rule_name, data in self.registered_ratios.items():
            lines.append(f'{rule_name} = "{data["symbol"]}"')

        # Add binary logical operators to grammar
        lines.append('')
        lines.append('# Binary logical operators rules')
        binary_boolean_operations_rule = f'binary_logical_operator = {" / ".join(self.registered_binary_logical_operators.keys())}'
        lines.append(binary_boolean_operations_rule)
        for rule_name, data in self.registered_binary_logical_operators.items():
            lines.append(f'{rule_name} = "{data["symbol"]}"')

        final_grammar = '\n'.join(lines)

        return final_grammar

    @property
    def grammar(self) -> Grammar:
        """
        The PEG grammar object used for encoding expressions
        :return: PEG grammar object
        """

        return Grammar(self._get_peg_format_grammar())

    """
    These visit_* functions are called by the encoder when it translates the raw PEG parse result
    into an Expression.
    For a more in depth explanation check out the parsimonious package documentation README
    """

    def visit_field(self, node: Node, visited_children: List) -> Field:
        return Field(name=node.text)

    def visit_number(self, node: Node, visited_children: List):
        return float(node.text)

    def visit_true(self, node: Node, visited_children: List) -> bool:
        return True

    def visit_false(self, node: Node, visited_children: List) -> bool:
        return False

    def visit_string(self, node: Node, visited_children: List) -> bool:
        matches = re.findall(r"^'(.*)'$", node.text)
        if len(matches) != 1:
            raise AssertionError(f'Expected regular expression of string to have one '
                                 f'match (found {len(matches)} matches), probably string '
                                 f'has an invalid format')
        value = matches[0]
        return value

    def visit_expression(self, node: Node, visited_children: List) -> Expression:
        # Ignore children that do not have an encoding
        # result (mostly spaces & symbols not needed in the resulting expression)
        _visited_children = [c for c in visited_children if c]
        _visited_children = _visited_children[0] if len(_visited_children) == 1 else _visited_children

        # The expression is always in the format: a operator b
        operator = _visited_children[1]
        a = _visited_children[0]
        b = _visited_children[2]

        if issubclass(operator, BooleanOperation):
            return operator(operands=[a, b])
        elif issubclass(operator, BinaryOperation):
            return operator(field=a, value=b)

        raise Exception(f'Unknown expression type. operator: {operator}')

    def generic_visit(self, node: Node, visited_children: List) -> List:

        # Basically pass the values from the children forward & ignore children with no encoding
        _visited_children = [c for c in visited_children if c]
        return _visited_children[0] if len(_visited_children) == 1 else _visited_children

    def encode_expression(self, expression: str) -> Expression:
        """
        Encode an unencoded expression into an Expression object representing the input
        :param expression: a string representing a boolean expression
        :return: an Expression representing the given expression string
        """

        encoded_expression = self.parse(expression)
        return encoded_expression
