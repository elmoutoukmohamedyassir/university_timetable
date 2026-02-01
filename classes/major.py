class Major :
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.groups=[] # Liste d'objets de type Groupe
        self.schedule = None
    def add_group(self, new_group):
        self.groups.append(new_group)
