from typing import Any, List

from pydantic import BaseModel


# An expression is a token that can be resolved to a boolean value
class Expression(BaseModel):
    pass


# A type of a boolean expression that sums up multiple boolean values (for example: and, or, xor)
class BooleanOperation(Expression):
    operands: List[Expression]


# A field of the queried object
class Field(BaseModel):
    name: str


# A type of boolean expression that evaluates a field against a value and returns a boolean result
class BinaryOperation(Expression):
    field: Field
    value: Any
