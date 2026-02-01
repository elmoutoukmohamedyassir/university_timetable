from user import User

class Administrator(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def show_menu(self):
        print("Administrator Menu")
