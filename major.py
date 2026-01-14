class Major :
    def __init__(self, name):
        self.name = name
        self.students = []
        self.courses = []
        self.groups=[] # Liste d'objets de type Groupe
        self.schedule = None
