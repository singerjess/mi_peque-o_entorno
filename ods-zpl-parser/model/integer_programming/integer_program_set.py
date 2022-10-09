class IntegerProgramSet:
    def __init__(self, name: str, set_range: list):
        self._name = name
        self._set_range = set_range

    def name(self):
        return self._name

    def set_range(self):
        return self._set_range
