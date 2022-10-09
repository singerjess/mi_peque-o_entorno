from enum import Enum


class Operator(Enum):
    EQUAL = '=='
    LESS_OR_EQUAL = '<='
    LESS = '<'


class Inequation:
    def __init__(self, left_side: [], right_side: str, operator: Operator):
        self.left_side = left_side
        self.right_side = right_side
        self.operator = operator
