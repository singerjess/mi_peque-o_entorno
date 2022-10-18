from model.classroom.course import Course
from model.classroom.spanish_day_of_week import DayOfWeek


class CourseClass:
    def __init__(self, course: Course, start_time: float, end_time: float, day: DayOfWeek):
        self.course = course
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __eq__(self, other):
        if isinstance(other, CourseClass):
            return other.course == self.course and other.start_time == self.start_time and other.end_time == self.end_time and other.day == self.day
        return False

    def __hash__(self):
        return (hash(self.course) ^ hash(self.start_time) ^ hash(self.end_time) ^ hash(
            self.day) ^ hash((self.course, self.start_time, self.end_time, self.day)))

    def does_not_intersect(self, another_class):
        return another_class.start_time >= self.end_time or another_class.end_time <= self.start_time or self.day != another_class.day

    def intersects(self, another_class):
        return not self.does_not_intersect(another_class)
