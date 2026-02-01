class Course:
    def __init__(self, name, course_type, needed_equipment="None"):
        self.name = name
        self.course_type = course_type  # Lecture, TD, TP, Exam
        if needed_equipment is None:
            self.needed_equipment = []
        else:
            self.needed_equipment = needed_equipment