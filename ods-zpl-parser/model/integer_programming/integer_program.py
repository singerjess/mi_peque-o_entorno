from model.integer_programming.inequation import Inequation


class IntegerProgram:
    _subject_to: [Inequation]

    def __init__(self, sets: [], all_vars: [], subject_to: [], objective_function: str):
        self._sets = sets
        self._vars = all_vars
        self._subject_to = subject_to
        self._objective_function = objective_function

    def subject_to(self) -> [Inequation]:
        return self._subject_to

    def objective_function(self):
        return self._objective_function

    def vars(self):
        return self._vars

    def sets(self):
        return self._sets
