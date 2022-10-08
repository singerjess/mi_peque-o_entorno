from model.classroom.course_class import CourseClass
from model.classroom.semester import Semester
from model.integer_programming.integer_program_set import IntegerProgramSet
from model.integer_programming.variable import Variable, VarType


class ClassroomAssignmentProblemMapper:
    def __init__(self, semester: Semester):
        self.semester = semester

    def map_to_representatives_problem(self):
        sets = []
        vars = []
        F = IntegerProgramSet("F", "1.." + str(len(self.semester.courses)))
        sets.append(F)
        courses_list = []
        classes_by_course = dict()


        course_classes_array = list(self.semester.course_classes)
        for index, course_class in enumerate(course_classes_array):
            non_intersected_classes = set({})
            for another_index, another_course_class in enumerate(course_classes_array):
                if index == another_index or self.classes_dont_intersect(another_course_class,
                                                                         course_class):
                    non_intersected_classes.add(another_index)
            sets.append(IntegerProgramSet("I"+str(index), str(non_intersected_classes)))
            vars.append(Variable("X[I"+str(index)+"]", "", VarType.BINARY))

        for course in self.semester.courses:
            courses_list.append(course)
            classes_of_course = []
            for index, course_class in enumerate(course_classes_array):
                if course_class.course == course:
                    classes_of_course.append(course_class)
            classes_by_course[course] = classes_of_course

        a = 4


    def classes_dont_intersect(self, another_course_class: CourseClass, course_class: CourseClass):
        return (
                another_course_class.start_time >= course_class.end_time or
                another_course_class.end_time <= course_class.start_time or
                another_course_class.day != course_class.day)

    def map_to_node_and_color_representation_problem(self):
        return 0
