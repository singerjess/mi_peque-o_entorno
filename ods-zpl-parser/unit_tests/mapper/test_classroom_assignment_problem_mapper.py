import pytest

from mapper.classroom_assignment_problem_mapper import ClassroomAssignmentProblemMapper
from model.classroom.course import Course
from model.classroom.course_class import CourseClass
from model.classroom.semester import Semester
from model.classroom.spanish_day_of_week import DayOfWeek


class TestClassroomAssignmentProblemMapper:
    def test_one_course_class_has_trivial_representatives_representation(self):
        course = Course(name="pintura", teacher="Miss Jess", building_number=2)
        course_class = CourseClass(course=course, start_time=0.4, end_time=0.5, day=DayOfWeek.JUEVES)
        semester = Semester(courses={course}, course_classes={course_class},
                            name="2050_post_apocalipsis", total_classrooms=3)

        classroom_assignment_problem_mapper = ClassroomAssignmentProblemMapper(semester)
        classroom_assignment_problem_mapper.map_to_representatives_problem()