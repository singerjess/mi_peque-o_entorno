class Course:
    def __init__(self, name: str, teacher: str, building_number: int):
        self.name = name
        self.teacher = teacher
        self.building_number = building_number

    def __eq__(self, other):
        if isinstance(other, Course):
            return other.name == self.name and other.teacher == self.teacher and \
                   other.building_number == self.building_number
        return False

    def __hash__(self):
        return hash((self.name, self.teacher, self.building_number))
