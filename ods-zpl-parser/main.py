import json
import logging

import unidecode as unidecode
from pyexcel_ods import get_data

from model.classroom.course import Course
from model.classroom.course_class import CourseClass
from model.classroom.semester import Semester
from model.classroom.spanish_day_of_week import DayOfWeek


def main() -> int:
    semesters = []
    total_classrooms = [21, 22, 18, 26, 15, 20, 18, 23, 19, 22, 15, 20, 1, 1]  # sacado del paper

    all_semesters_json_data = parse_ods_file()
    i = 0
    for semester_key in all_semesters_json_data.keys():
        classes = []
        courses = []
        semester0 = Semester(set({}), [], semester_key + "_pabellon1", total_classrooms[i])
        semester1 = Semester(set({}), [], semester_key + "_pabellon2", total_classrooms[i + 1])
        i += 2
        classes_json_data = all_semesters_json_data[semester_key]
        parse_course_and_class(classes, classes_json_data, courses)
        get_semester_for_both_buildings(classes, semester0, semester1)
        semesters.append(semester0)
        semesters.append(semester1)

    for sem_index, semester in enumerate(semesters):
        ady_matrix = semester.get_classes_adjancency_matrix()
        courses_matrix = semester.get_matrix_of_courses()
        clases_by_course = semester.classes_by_course()
        amount_per_course = []
        for index, course in enumerate(semester.courses):
            amount_per_course.append(len(clases_by_course[index]))

        first_of_each_course = semester.get_first_of_each_course()

        with open("../scipoptsuite-8.0.1/test_cases/aux/reps/ady_matrix_" + str(sem_index) + ".txt",
                  "w") as file1:
            # Writing data to a file
            file1.write(format_matrix(ady_matrix))
        with open("../scipoptsuite-8.0.1/test_cases/aux/reps/data_" + str(sem_index) + ".txt",
                  "w") as file1:
            # Writing data to a file
            file1.write("clases: " + str(len(semester.course_classes)) + ", cursos: " + str(
                len(semester.courses)))
        with open("../scipoptsuite-8.0.1/test_cases/aux/reps/courses_matrix_" + str(sem_index) +
                  ".txt",
                  "w") as file1:
            # Writing data to a file
            file1.write(format_matrix(courses_matrix))
        with open("../scipoptsuite-8.0.1/test_cases/aux/reps/amount_per_course_" + str(sem_index) +
                  ".txt",
                  "w") as file1:
            logging.error(len(amount_per_course))
            file1.write(list_to_string(amount_per_course))

        with open(
                "../scipoptsuite-8.0.1/test_cases/aux/reps/first_of_each_course_" + str(
                    sem_index) + ".txt",
                "w") as file1:
            # Writing data to a file
            file1.write(list_to_string(first_of_each_course))
    return 0


0


def format_matrix(matrix):
    matrix_string = ""
    for row in matrix:
        row_str = ""
        for number in row:
            row_str += str(number) + " "
        row_str = row_str[:-1]
        matrix_string += row_str + "\n"
    return matrix_string


def list_to_string(a_list):
    list_string = ""
    for number in a_list:
        list_string += str(number) + " "

    return list_string[:-1]


# def porqueria() -> int:
#     semesters = []
#     total_classrooms = [21, 22, 18, 26, 15, 20, 18, 23, 19, 22, 15, 20, 1, 1]  # sacado del paper
#
#     all_semesters_json_data = parse_ods_file()
#     i = 0
#     for semester_key in all_semesters_json_data.keys():
#         classes = []
#         courses = set({})
#         semester0 = Semester(set({}), [], semester_key + "_pabellon1", total_classrooms[i])
#         semester1 = Semester(set({}), [], semester_key + "_pabellon2", total_classrooms[i + 1])
#         i += 2
#         classes_json_data = all_semesters_json_data[semester_key]
#         parse_course_and_class(classes, classes_json_data, courses)
#         get_semester_for_both_buildings(classes, semester0, semester1)
#         semesters.append(semester0)
#         semesters.append(semester1)
#
#     for semester in semesters:
#         ady_matrix = semester.get_classes_adjancency_matrix()
#         integer_problem = classroom_assignment_problem_mapper.map()
#         integer_program_zimpl_mapper = IntegerProgramZimplMapper()
#         result_string = integer_program_zimpl_mapper.map(integer_problem)
#         with open("resources/representatives_problem.zpl", "w") as file1:
#             # Writing data to a file
#             file1.write(result_string)
#         with open("resources/otracosa.zpl", "w") as file1:
#             for index, course_class in enumerate(semester.course_classes):
#                 # Writing data to a file
#                 file1.write(course_class.course.name + ", " + course_class.day.value + ", " +
#                                     course_class.course.teacher + ", " + str(
#                     course_class.start_time) + "\n")
#             break
#     return 0


def parse_ods_file():
    all_semesters_data = get_data("resources/instancias.ods")
    all_semesters_json_data = json.loads(json.dumps(all_semesters_data))
    return all_semesters_json_data


def get_semester_for_both_buildings(classes, semester0, semester1):
    for course_class in classes:
        if course_class.course.building_number == 1:
            semester0.course_classes.append(course_class)
            semester0.courses.add(course_class.course)  # no hay cursos sin clases
        else:
            semester1.course_classes.append(course_class)
            semester1.courses.add(course_class.course)


def parse_course_and_class(classes: [], classes_json_data, courses):
    for class_data in classes_json_data:
        course = Course(name=class_data[0], teacher=str(class_data[2]),
                        building_number=class_data[10])
        if course not in courses:
            courses.append(course)
        if class_data[4] != "":
            classes.append(CourseClass(course=course,
                                       day=DayOfWeek[unidecode.unidecode(class_data[4]).upper()],
                                       start_time=class_data[6], end_time=class_data[8]))


if __name__ == '__main__':
    main()
