class Course:
    def __init__(self, id, name, type, teacher, groups, attendees, needed_equipment):
        self.id = id
        self.name = name
        self.type = type
        self.teacher = teacher
        self.groups = groups
        self.attendees = attendees
        self.needed_equipment = needed_equipment
        self.time_slot = None
        self.room = None