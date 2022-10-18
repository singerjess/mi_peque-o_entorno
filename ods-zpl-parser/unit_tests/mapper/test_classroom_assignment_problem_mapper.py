from mapper.classroom_assignment_representatives_problem_mapper import \
    ClassroomAssignmentRepresentativesProblemMapper
from mapper.integer_program_zimpl_mapper import IntegerProgramZimplMapper
from model.classroom.course import Course
from model.classroom.course_class import CourseClass
from model.classroom.semester import Semester
from model.classroom.spanish_day_of_week import DayOfWeek


class TestClassroomAssignmentProblemMapper:
    def test_one_course_class_has_trivial_representatives_representation(self):
        course = Course(name="pintura", teacher="Miss Jess", building_number=2)
        course_class = CourseClass(course=course, start_time=0.5, end_time=0.6,
                                   day=DayOfWeek.MIERCOLES)
        semester = Semester(courses={course}, course_classes={course_class},
                            name="2050_post_apocalipsis", total_classrooms=3)

        classroom_assignment_problem_mapper = ClassroomAssignmentRepresentativesProblemMapper(
            semester)
        integer_problem = classroom_assignment_problem_mapper.map()

        assert len(integer_problem.vars()) == 2
        assert integer_problem.vars()[0].name() == "x_IJ"
        assert integer_problem.vars()[1].name() == "z[F]"
        assert len(integer_problem.sets()) == 2
        assert integer_problem.sets()[0].name() == "I0"
        assert integer_problem.sets()[1].name() == "F"
        assert len(integer_problem.subject_to()) == 4
        assert integer_problem.objective_function() == "sum <f> in F : z[f]"

    def test_one_course_with_two_classes_has_two_colors_if_they_overlap(self):
        course = Course(name="pintura", teacher="Miss Jess", building_number=2)
        course_class_1 = CourseClass(course=course, start_time=0.5, end_time=0.6,
                                     day=DayOfWeek.MIERCOLES)
        course_class_2 = CourseClass(course=course, start_time=0.5, end_time=0.65,
                                     day=DayOfWeek.MIERCOLES)
        semester = Semester(courses={course}, course_classes={course_class_1, course_class_2},
                            name="2050_post_apocalipsis", total_classrooms=3)

        classroom_assignment_problem_mapper = ClassroomAssignmentRepresentativesProblemMapper(
            semester)
        integer_problem = classroom_assignment_problem_mapper.map()

        assert len(integer_problem.vars()) == 3
        assert integer_problem.vars()[0].name() == "x_0[I0]"
        assert integer_problem.vars()[1].name() == "x_1[I1]"
        assert integer_problem.vars()[2].name() == "z[F]"
        assert len(integer_problem.sets()) == 3
        assert integer_problem.sets()[0].name() == "I0"
        assert integer_problem.sets()[0].set_range() == [0]
        assert integer_problem.sets()[1].name() == "I1"
        assert integer_problem.sets()[1].set_range() == [1]
        assert integer_problem.sets()[2].name() == "F"
        assert integer_problem.sets()[2].set_range() == [0]
        assert len(integer_problem.subject_to()) == 6
        assert integer_problem.objective_function() == "sum <f> in F : z[f]"

        integer_program_zimpl_mapper = IntegerProgramZimplMapper()
        result_string = integer_program_zimpl_mapper.map(integer_problem)
        with open("../resources/demofile2.zpl", "w") as file1:
            # Writing data to a file
            file1.write(result_string)


    def test_one_course_with_two_classes_has_two_colors_if_they_dont_overlap(self):
        course = Course(name="pintura", teacher="Miss Jess", building_number=2)
        course_class_1 = CourseClass(course=course, start_time=0.5, end_time=0.6,
                                     day=DayOfWeek.MIERCOLES)
        course_class_2 = CourseClass(course=course, start_time=0.6, end_time=0.65,
                                     day=DayOfWeek.MIERCOLES)
        course_class_3 = CourseClass(course=course, start_time=0.66, end_time=0.75,
                                     day=DayOfWeek.JUEVES)
        semester = Semester(courses={course}, course_classes={course_class_1, course_class_2, course_class_3},
                            name="2050_post_apocalipsis", total_classrooms=3)

        classroom_assignment_problem_mapper = ClassroomAssignmentRepresentativesProblemMapper(
            semester)
        integer_problem = classroom_assignment_problem_mapper.map()

        assert len(integer_problem.vars()) == 4
        assert integer_problem.vars()[0].name() == "x_0[I0]"
        assert integer_problem.vars()[1].name() == "x_1[I1]"
        assert integer_problem.vars()[3].name() == "z[F]"
        assert len(integer_problem.sets()) == 4
        assert integer_problem.sets()[0].name() == "I0"
        assert integer_problem.sets()[0].set_range() == [0, 1,2]
        assert integer_problem.sets()[1].name() == "I1"
        assert integer_problem.sets()[1].set_range() == [1, 0,2]
        assert integer_problem.sets()[3].name() == "F"
        assert integer_problem.sets()[3].set_range() == [0]
        assert len(integer_problem.subject_to()) == 8
        assert integer_problem.objective_function() == "sum <f> in F : z[f]"

        integer_program_zimpl_mapper = IntegerProgramZimplMapper()
        result_string = integer_program_zimpl_mapper.map(integer_problem)
        with open("../resources/demofile2.zpl", "w") as file1:
            # Writing data to a file
            file1.write(result_string)

    def test_two_course_with_three_classes_has_two_colors_if_they_dont_overlap(self):
        course = Course(name="pintura", teacher="Miss Jess", building_number=2)
        course_class_1 = CourseClass(course=course, start_time=0.5, end_time=0.6,
                                     day=DayOfWeek.MIERCOLES)
        course_class_2 = CourseClass(course=course, start_time=0.6, end_time=0.65,
                                     day=DayOfWeek.MIERCOLES)
        course_class_3 = CourseClass(course=course, start_time=0.60, end_time=0.75,
                                     day=DayOfWeek.MIERCOLES)
        crochet_course = Course(name="crochet", teacher="Miss Jessi", building_number=2)
        crochet_class_1 = CourseClass(course=crochet_course, start_time=0.5, end_time=0.6,
                                     day=DayOfWeek.MIERCOLES)
        crochet_class_2 = CourseClass(course=crochet_course, start_time=0.6, end_time=0.65,
                                     day=DayOfWeek.MIERCOLES)
        crochet_class_3 = CourseClass(course=crochet_course, start_time=0.66, end_time=0.75,
                                     day=DayOfWeek.JUEVES)
        semester = Semester(courses={course, crochet_course}, course_classes=[course_class_1,
                                                                              course_class_2,
                                                              course_class_3, crochet_class_1,
                                                              crochet_class_2, crochet_class_3],
                            name="2050_post_apocalipsis", total_classrooms=3)

        classroom_assignment_problem_mapper = ClassroomAssignmentRepresentativesProblemMapper(
            semester)
        integer_problem = classroom_assignment_problem_mapper.map()


        integer_program_zimpl_mapper = IntegerProgramZimplMapper()
        result_string = integer_program_zimpl_mapper.map(integer_problem)
        with open("../resources/demofile2.zpl", "w") as file1:
            # Writing data to a file
            file1.write(result_string)
