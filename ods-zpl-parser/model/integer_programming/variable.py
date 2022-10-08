from enum import Enum


class VarType(Enum):
    INTEGER = 0
    BINARY = 1


class Variable:
    def __init__(self, name: str, restrictions: str, var_type: VarType):
        self.name = name
        self.restrictions = restrictions
        self.var_type = var_type
