from enum import Enum


class VarType(Enum):
    INTEGER = 'integer'
    BINARY = 'binary'


class Variable:
    def __init__(self, name: str, restrictions: str, var_type: VarType):
        self._name = name
        self._restrictions = restrictions
        self._var_type = var_type

    def name(self):
        return self._name

    def restrictions(self):
        return self._restrictions

    def var_type(self):
        return self._var_type
