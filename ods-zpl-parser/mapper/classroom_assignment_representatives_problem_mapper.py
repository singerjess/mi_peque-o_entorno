from model.classroom.course_class import CourseClass
from model.classroom.semester import Semester
from model.integer_programming.inequation import Inequation, Operator
from model.integer_programming.integer_program import IntegerProgram
from model.integer_programming.integer_program_set import IntegerProgramSet
from model.integer_programming.variable import Variable, VarType


class ClassroomAssignmentRepresentativesProblemMapper:
    def __init__(self, semester: Semester):
        self.semester = semester

    def map(self) -> IntegerProgram:
        x_sets = []
        x_vars = []
        inequalities = []
        F_set = IntegerProgramSet("F", list(range(0, len(self.semester.courses))))
        course_classes_array = list(self.semester.course_classes)
        courses_list = list(self.semester.courses)
        z_var = Variable("z[F]", "", VarType.BINARY)
        self.create_x_sets_and_vars(course_classes_array, x_sets, x_vars)

        classes_by_course = self.get_classes_by_course(course_classes_array, courses_list)
        z_f_inequalities = self.generate_z_f_inequalities(classes_by_course, courses_list, x_sets)
        non_neighbor_inequalities = self.create_non_neighbor_inequalities(x_sets, x_vars)
        non_neighbor_edges_inequalities = self.create_non_neighbor_edges_inequalities(x_sets,
                                                                                        x_vars)
        feasibility_inequality = self.create_feasibility_inequality(x_vars,
                                                                    self.semester.total_classrooms)
        rep_feasible_inequalities = self.create_rep_feasibility_inequalities(x_sets, x_vars)
        inequalities.extend(rep_feasible_inequalities)
        inequalities.extend(z_f_inequalities)
        inequalities.extend(non_neighbor_edges_inequalities)
        inequalities.extend(non_neighbor_inequalities)
        inequalities.append(feasibility_inequality)
        objective_function = "sum <f> in F : z[f]"
        all_sets = x_sets + [F_set]
        all_vars = x_vars + [z_var]
        return IntegerProgram(all_sets, all_vars, inequalities, objective_function)

    def create_non_neighbor_edges_inequalities(self, x_sets, x_vars):

        non_neighbors_edges_inequalities = []
        for index, x_var in enumerate(x_vars):
            right_side = "x_" + str(index) + "[" + str(index) + "]"
            for non_neighbor in x_sets[index].set_range():
                for another_non_neighbor in x_sets[index].set_range():
                    if non_neighbor != index and another_non_neighbor != index and self.vertices_are_connected(
                            another_non_neighbor, non_neighbor, x_sets):
                        left_side = "x_" + str(index) + "[" + str(non_neighbor) + "]" + " + x_" + \
                                    str(
                            index) + "[" + str(another_non_neighbor) + "]"
                        non_neighbors_edges_inequalities.append(
                            Inequation(left_side, right_side, Operator.LESS_OR_EQUAL))

        return non_neighbors_edges_inequalities

    def create_rep_feasibility_inequalities(self, x_sets, x_vars):
        # para que cada uno lo represente uno solo
        rep_feasible_inequalities = []
        for index, x_var in enumerate(x_vars):
            left_side = ""
            for non_neighbor in x_sets[index].set_range():
                left_side += "x_" + str(non_neighbor) + "[" + str(index) + "]" + " + "
            left_side = left_side[:-3]
            rep_feasible_inequalities.append(
                Inequation(left_side, "1", Operator.EQUAL))

        return rep_feasible_inequalities

    def vertices_are_connected(self, another_non_neighboor, non_neighboor, x_sets):
        return non_neighboor not in x_sets[another_non_neighboor]._set_range

    def create_non_neighbor_inequalities(self, x_sets, x_vars):
        non_neighbors_inequalities = []
        for index, x_var in enumerate(x_vars):
            right_side = ""
            for non_neighbor in x_sets[index].set_range():
                right_side += "x_" + str(non_neighbor) + "[" + str(index) + "] + "
            right_side = right_side[:-3]
            if right_side != "":
                non_neighbors_inequalities.append(
                    Inequation("1", right_side, Operator.LESS_OR_EQUAL))
        return non_neighbors_inequalities

    def generate_z_f_inequalities(self, classes_by_course, courses_list, x_sets):
        inequalities = []
        for index, course in enumerate(courses_list):
            left_side = str(len(classes_by_course[index])) + " * " + "z[" + str(index) + "]"
            right_side = ""

            should_break_chanchada = False
            for class_1 in classes_by_course[index]:
                for class_2 in classes_by_course[index]:
                    if class_2 not in x_sets[class_1].set_range():
                        should_break_chanchada = True
            if should_break_chanchada:
                inequalities.append(Inequation(left_side, "0", Operator.EQUAL))
                continue
            # for class_of_course in classes_by_course[index]: romper la simetria
            if len(classes_by_course[index]) > 0:
                selected_class = classes_by_course[index][0] # romper la simetria
                for another_class_of_course in classes_by_course[index]:
                    right_side += "x_" + str(selected_class) + "[" + str(
                        another_class_of_course) + "] + "
            right_side = right_side[:-3]

            z_f_inequality = Inequation(left_side, right_side, Operator.LESS_OR_EQUAL)
            inequalities.append(z_f_inequality)
        return inequalities

    def create_x_sets_and_vars(self, course_classes_array, sets, vars):
        for index, course_class in enumerate(course_classes_array):
            non_intersected_classes = [index]
            for another_index, another_course_class in enumerate(course_classes_array):
                if self.classes_dont_intersect(another_course_class, course_class):
                    non_intersected_classes.append(another_index)
            sets.append(IntegerProgramSet("I" + str(index), non_intersected_classes))
            vars.append(Variable(self.x_variable_string(index), "", VarType.BINARY))

    def x_variable_string(self, index):
        return "x_" + str(index) + "[I" + str(index) + "]"

    def get_classes_by_course(self, course_classes_array, courses_list):
        classes_by_course = dict()
        for course_index, course in enumerate(courses_list):
            classes_of_course = []
            for index, course_class in enumerate(course_classes_array):
                if course_class.course == course:
                    classes_of_course.append(index)
            classes_by_course[course_index] = classes_of_course
        return classes_by_course

    def classes_dont_intersect(self, another_course_class: CourseClass, course_class: CourseClass):
        return (
                another_course_class.start_time >= course_class.end_time or another_course_class.end_time <= course_class.start_time or another_course_class.day != course_class.day)

    def create_feasibility_inequality(self, x_vars: [], total_classrooms: int):
        right_side = str(total_classrooms)
        left_side = ""
        for index, x_var in enumerate(x_vars):
            left_side += "x_" + str(index) + "[" + str(index) + "] + "
        left_side = left_side[:-2]
        return Inequation(left_side, right_side, Operator.LESS_OR_EQUAL)
