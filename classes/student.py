from user import User

class Student(User):
    def __init__(self, user_id, name, major, group):
        super().__init__(user_id, name)
        self.major = major
        self.group = group

    def show_menu(self):
        print("Student Menu")
