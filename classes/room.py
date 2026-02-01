class Room:
    def __init__(self, name, capacity, equipment, room_type="Classroom"):
        self.name = name
        self.capacity = capacity
        self.equipment = equipment  # list of strings
        self.room_type = room_type  # e.g., 'Classroom', 'Lab', 'Amphitheater'
