class Course:
    def __init__(self, name, course_type, students, needed_equipment=None):
        self.name = name
        self.course_type = course_type
        self.students = students
        if needed_equipment is None:
            self.needed_equipment = []
        else:
            self.needed_equipment = needed_equipment

    def __str__(self):
        return f"{self.name} ({self.course_type})"