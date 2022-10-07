class Semester:
    def __init__(self, courses: set, course_classes: set, name: str, total_classrooms: int):
        self.courses = courses
        self.course_classes = course_classes
        self.name = name
        self.total_classrooms = total_classrooms
