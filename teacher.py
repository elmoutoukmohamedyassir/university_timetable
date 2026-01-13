from user import User

class Teacher(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.unavailable_slots = []

    def show_menu(self):
        print("Teacher Menu")

    def add_unavailability(self, timeslot):
        self.unavailable_slots.append(timeslot)
