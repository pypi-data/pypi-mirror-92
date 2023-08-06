from jijmodeling.expression.expression import Operator


class Condition(Operator):
    def __and__(self, other):
        return AndOperator([self, other])

    def __xor__(self, other):
        return XorOperator([self, other])

    def __or__(self, other):
        return OrOperator([self, other])


class Equal(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] == objects[1]

    def __repr__(self) -> str:
        return '{} == {}'.format(self.children[0], self.children[1])


class NotEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] != objects[1]

    def __repr__(self) -> str:
        return '{} != {}'.format(self.children[0], self.children[1])


class LessThan(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] < objects[1]

    def __repr__(self) -> str:
        return '{} < {}'.format(self.children[0], self.children[1])


class LessThanEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] <= objects[1]

    def __repr__(self) -> str:
        return '{} <= {}'.format(self.children[0], self.children[1])


class GreaterThan(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] > objects[1]

    def __repr__(self) -> str:
        return '{} > {}'.format(self.children[0], self.children[1])


class GreaterThanEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] >= objects[1]

    def __repr__(self) -> str:
        return '{} >= {}'.format(self.children[0], self.children[1])


class AndOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] & objects[1]

    def __repr__(self) -> str:
        return '{} & {}'.format(self.children[0], self.children[1])


class XorOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] ^ objects[1]

    def __repr__(self) -> str:
        return '({}) xor ({})'.format(self.children[0], self.children[1])


class OrOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] | objects[1]

    def __repr__(self) -> str:
        return '({}) | ({})'.format(self.children[0], self.children[1])


def equal(left, right) -> Equal:
    return Equal([left, right])


def eq(left, right) -> Equal:
    return equal(left, right)


def neq(left, right) -> NotEqual:
    return NotEqual([left, right])
