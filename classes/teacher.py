from user import User

class Teacher(User):
    def __init__(self, user_id, name, max_hours=20):
        super().__init__(user_id, name)
        self.unavailable_slots = []

        self.max_hours = max_hours

    def show_menu(self):
        print("Teacher Menu")

    def add_unavailability(self, timeslot):
        self.unavailable_slots.append(timeslot)
