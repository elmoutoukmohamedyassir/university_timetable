class Group:
    def __init__(self, name, capacity, major):
        self.name = name
        self.capacity = capacity
        self.major = major  
        self.students = []  
        self.schedule = None

    def add_student(self, student):
        if len(self.students) < self.capacity:
            self.students.append(student)
            return True
        return False
