from user import User

class Student(User):
    def __init__(self, user_id, name, program, group):
        super().__init__(user_id, name)
        self.program = program
        self.group = group

    def show_menu(self):
        print("Student Menu")
