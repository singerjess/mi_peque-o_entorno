import json

import unidecode as unidecode

from mapper.classroom_assignment_representatives_problem_mapper import \
    ClassroomAssignmentRepresentativesProblemMapper
from mapper.integer_program_zimpl_mapper import IntegerProgramZimplMapper
from model.classroom.course import Course
from model.classroom.course_class import CourseClass
from pyexcel_ods import get_data

from model.classroom.semester import Semester
from model.classroom.spanish_day_of_week import DayOfWeek


def main() -> int:
    """Echo the input arguments to standard output"""

    semesters = []
    total_classrooms = [21, 22, 18, 26, 15, 20, 18, 23, 19, 22, 15, 20, 1, 1]  # sacado del paper

    all_semesters_json_data = parse_ods_file()
    i = 0
    for semester_key in all_semesters_json_data.keys():
        classes = set({})
        courses = set({})
        semester0 = Semester(set({}), set({}), semester_key + "_pabellon1", total_classrooms[i])
        semester1 = Semester(set({}), set({}), semester_key + "_pabellon2", total_classrooms[i + 1])
        i += 2
        classes_json_data = all_semesters_json_data[semester_key]
        parse_course_and_class(classes, classes_json_data, courses)
        get_semester_for_both_buildings(classes, semester0, semester1)
        semesters.append(semester0)
        semesters.append(semester1)
    for semester in semesters:
        classroom_assignment_problem_mapper = ClassroomAssignmentRepresentativesProblemMapper(
            semester)
        integer_problem = classroom_assignment_problem_mapper.map()
        integer_program_zimpl_mapper = IntegerProgramZimplMapper()
        result_string = integer_program_zimpl_mapper.map(integer_problem)
        with open("resources/demofile2.zpl", "w") as file1:
            # Writing data to a file
            file1.write(result_string)
            break
    return 0


def parse_ods_file():
    all_semesters_data = get_data("resources/instancias.ods")
    all_semesters_json_data = json.loads(json.dumps(all_semesters_data))
    return all_semesters_json_data


def get_semester_for_both_buildings(classes, semester0, semester1):
    for course_class in classes:
        if course_class.course.building_number == 1:
            semester0.course_classes.add(course_class)
            semester0.courses.add(course_class.course)  # no haycursos sin clases
        else:
            semester1.course_classes.add(course_class)
            semester1.courses.add(course_class.course)


def parse_course_and_class(classes, classes_json_data, courses):
    for class_data in classes_json_data:
        course = Course(name=class_data[0], teacher=class_data[2], building_number=class_data[10])
        courses.add(course)
        if class_data[4] != "":
            classes.add(CourseClass(course=course,
                                    day=DayOfWeek[unidecode.unidecode(class_data[4]).upper()],
                                    start_time=class_data[6], end_time=class_data[8]))


if __name__ == '__main__':
    main()
