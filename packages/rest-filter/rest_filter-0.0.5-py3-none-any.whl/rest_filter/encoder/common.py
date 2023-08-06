from .encoder import Encoder
from .base_types import BooleanOperation, BinaryOperation

# This is an encoder "pre loaded" with common logical operators & ratios.
# Basically a "Good enough to start with" encoder
encoder = Encoder()


@encoder.register_binary_logical_operator('and')
class And(BooleanOperation):
    pass


@encoder.register_binary_logical_operator('or')
class Or(BooleanOperation):
    pass


@encoder.register_ratio('gt')
class GraterThan(BinaryOperation):
    pass


@encoder.register_ratio('ge')
class GraterEqualsTo(BinaryOperation):
    pass


@encoder.register_ratio('lt')
class LessThan(BinaryOperation):
    pass


@encoder.register_ratio('le')
class LessEqualsTo(BinaryOperation):
    pass


@encoder.register_ratio('eq')
class Equals(BinaryOperation):
    pass


@encoder.register_ratio('ne')
class NotEquals(BinaryOperation):
    pass
