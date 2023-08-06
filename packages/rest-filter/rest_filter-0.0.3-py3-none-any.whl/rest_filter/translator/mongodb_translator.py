from typing import Dict, List

from rest_filter.encoder import BinaryOperation, BooleanOperation, Expression
from rest_filter.encoder.common import (
    And, Or,
    GraterThan, GraterEqualsTo, LessThan, LessEqualsTo,
    Equals, NotEquals
)


class MongoTranslator:
    """
    A translator from encoded boolean expressions into a raw mongo filter
    """

    binary_operation_translators: List[Dict] = []
    boolean_operation_translators: List[Dict] = []

    def translate(self, encoded_expression: Expression) -> Dict:
        """
        Translates an expression into a mongo filter
        :param encoded_expression: The boolean expression to translate
        :return: A mongo filter dict
        """

        if isinstance(encoded_expression, BinaryOperation):

            # Check that list of registered binary operations to find one
            # that matches to the expression. if found, translate using the match
            for translator_info in self.binary_operation_translators:
                cls = translator_info['class']
                translator = translator_info['translator']

                if isinstance(encoded_expression, cls):
                    return translator(encoded_expression)

            raise Exception(f'Unknown binary operation type: {type(encoded_expression)}')

        elif isinstance(encoded_expression, BooleanOperation):

            # Check that list of registered boolean operations to find one
            # that matches to the expression. if found, translate using the match
            for translator_info in self.boolean_operation_translators:
                cls = translator_info['class']
                translator = translator_info['translator']

                if isinstance(encoded_expression, cls):
                    return translator(encoded_expression, self)

            raise Exception(f'Unknown boolean operation type: {type(encoded_expression)}')

        raise Exception(f'Unknown expression type: {type(encoded_expression)}')

    def register_binary_operation_translator(self, binary_operation: BinaryOperation):
        """
        Register a translation function from encoded form into mongo filter
        :param binary_operation: The encoded binary operation type that matches this translation
        :return: A decorator for the translation function
        """

        def decorator(func):

            # Make sure that the given class isn't registered as a translator already
            for translator_info in self.binary_operation_translators:
                cls = translator_info['class']
                if issubclass(binary_operation, cls):
                    raise Exception(f'The translator class {binary_operation} superseded '
                                    f'by existing translator class {cls}')

            self.binary_operation_translators.append({
                'class': binary_operation,
                'translator': func
            })

            return func

        return decorator

    def register_boolean_operation_translator(self, boolean_operation: BooleanOperation):
        """
        Register a translation function from encoded form into mongo filter
        :param boolean_operation: The encoded boolean operation type that matches this translation
        :return: A decorator for the translation function
        """

        def decorator(func):

            # Make sure that the given class isn't registered as a translator already
            for translator_info in self.boolean_operation_translators:
                cls = translator_info['class']
                if issubclass(boolean_operation, cls):
                    raise Exception(f'The translator class {boolean_operation} superseded '
                                    f'by existing translator class {cls}')

            self.boolean_operation_translators.append({
                'class': boolean_operation,
                'translator': func
            })

            return func

        return decorator


mongo_translator = MongoTranslator()


@mongo_translator.register_boolean_operation_translator(And)
def translate_and(operation: And, translator: MongoTranslator):
    return {
        '$and': [
            translator.translate(operand) for operand in operation.operands
        ]
    }


@mongo_translator.register_boolean_operation_translator(Or)
def translate_or(operation: Or, translator: MongoTranslator):
    return {
        '$or': [
            translator.translate(operand) for operand in operation.operands
        ]
    }


@mongo_translator.register_binary_operation_translator(Equals)
def translate_equals(operation: Equals):
    return {
        operation.field.name: {
            '$eq': operation.value
        }
    }


@mongo_translator.register_binary_operation_translator(NotEquals)
def translate_not_equals(operation: NotEquals):
    return {
        operation.field.name: {
            '$ne': operation.value
        }
    }


@mongo_translator.register_binary_operation_translator(GraterThan)
def translate_grater_than(operation: GraterThan):
    return {
        operation.field.name: {
            '$gt': operation.value
        }
    }


@mongo_translator.register_binary_operation_translator(GraterEqualsTo)
def translate_grater_than(operation: GraterEqualsTo):
    return {
        operation.field.name: {
            '$ge': operation.value
        }
    }


@mongo_translator.register_binary_operation_translator(LessThan)
def translate_less_than(operation: LessThan):
    return {
        operation.field.name: {
            '$lt': operation.value
        }
    }


@mongo_translator.register_binary_operation_translator(LessEqualsTo)
def translate_less_than(operation: LessEqualsTo):
    return {
        operation.field.name: {
            '$le': operation.value
        }
    }
