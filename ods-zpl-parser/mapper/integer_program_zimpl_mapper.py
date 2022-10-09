from model.integer_programming.integer_program import IntegerProgram


class IntegerProgramZimplMapper:
    def map(self, integer_program: IntegerProgram):
        result = ""
        result = self.add_sets_string(integer_program, result)
        result = self.add_var_string(integer_program, result)
        result = self.add_objective_function_string(integer_program, result)
        result = self.add_subject_to_string(integer_program, result)
        return result

    def add_subject_to_string(self, integer_program, result):
        for index, ineq in enumerate(integer_program.subject_to()):
            result += "subto " + "name_" + str(
                index) + ": " + ineq.left_side + " " + ineq.operator.value + " " + ineq.right_side + '; \n'
        return result

    def add_objective_function_string(self, integer_program, result):
        return result + "maximize pepe: " + integer_program.objective_function() + ';\n'

    def add_var_string(self, integer_program, result):
        for integer_program_var in integer_program.vars():
            result += "var "
            result += integer_program_var.name() + " " + integer_program_var.var_type().value + ";\n"
        return result

    def add_sets_string(self, integer_program, result):
        for integer_program_set in integer_program.sets():
            result += "set " + integer_program_set.name() + " := {"
            for set_number in integer_program_set.set_range():
                result += str(set_number) + ", "
            result = result[:-2]
            result += "}; \n"
        return result
