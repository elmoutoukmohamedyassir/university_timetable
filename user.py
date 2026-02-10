class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Admin(User):
    def __init__(self, id, name, email):
        super().__init__(id, name, email)
        

class Teacher(User):
    def __init__(self, id, name, email):
        super().__init__(id, name, email)
        self.availability = []
        self.unavailability = []

class Student(User):
    def __init__(self, id, name, email, group):
        super().__init__(id, name, email)
        self.group = group
