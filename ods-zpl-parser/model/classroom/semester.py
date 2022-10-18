from model.classroom.course import Course
from model.classroom.course_class import CourseClass


class Semester:
    def __init__(self, courses: [Course], course_classes: [CourseClass], name: str,
                 total_classrooms: int):
        self.courses = courses
        self.course_classes = course_classes
        self.name = name
        self.total_classrooms = total_classrooms

    def get_classes_adjancency_matrix(self):
        ady_matrix = [[0 for x in range(len(self.course_classes))] for y in
                      range(len(self.course_classes))]

        for index, _class in enumerate(self.course_classes):
            for another_index, _another_class in enumerate(self.course_classes):
                if _class.intersects(_another_class):
                    ady_matrix[index][another_index] = 1
                    ady_matrix[another_index][index] = 1
                else:
                    ady_matrix[index][another_index] = 0
                    ady_matrix[another_index][index] = 0
        return ady_matrix

    def get_matrix_of_courses(self):
        courses_matrix = [[0 for _ in range(len(self.course_classes))] for _ in
                          range(len(self.courses))]

        for index, course in enumerate(self.courses):
            for another_index, _class in enumerate(self.course_classes):
                if _class.course == course:
                    courses_matrix[index][another_index] = 1
        return courses_matrix

    def get_first_of_each_course(self):
        first_of_each_course = [-1 for x in range(len(self.courses))]

        for index, course in enumerate(self.courses):
            for another_index, _class in enumerate(self.course_classes):
                if _class.course == course:
                    first_of_each_course[index] = another_index
                    break
        return first_of_each_course

    def classes_by_course(self):
        classes_by_course = {}
        for course_index, course in enumerate(self.courses):
            classes_of_course = []
            for index, course_class in enumerate(self.course_classes):
                if course_class.course == course:
                    classes_of_course.append(index)
            classes_by_course[course_index] = classes_of_course
        return classes_by_course
