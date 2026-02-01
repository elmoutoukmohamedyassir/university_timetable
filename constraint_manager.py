class ConstraintManager:
    def __init__(self, schedule):
          self.schedule = schedule
    def check_room_conflict(self, new_session):#constant 1:Une salle ne peut pas être occupée par deux séances en même temps
        for session in self.schedule.sessions:
            if (
                session.room == new_session.room and
                session.timeslot.day == new_session.timeslot.day and
                session.timeslot.start_time == new_session.timeslot.start_time
            ):
                print("Conflit : salle déjà occupée")
                return True
        return False
    def check_teacher_conflict(self, new_session):#constant 2:Un enseignant ne peut pas être dans deux salles en même temps
        for session in self.schedule.sessions:
            if (
                session.teacher == new_session.teacher and
                session.timeslot.day == new_session.timeslot.day and
                session.timeslot.start_time == new_session.timeslot.start_time
            ):
                print("Conflit : enseignant indisponible")
                return True
        return False
    def check_group_conflict(self, new_session):#constant 3:Un groupe d’étudiants ne peut pas suivre deux séances en même temps
        for session in self.schedule.sessions:
            if (
                session.groupe == new_session.groupe and
                session.timeslot.overlaps(new_session.timeslot)
            ):
                print("Conflit : groupe déjà occupé")
                return True
        return False
    def check_teacher_availability(self, new_session):#constant 4:Respect des disponibilités de l’enseignant
        for slot in new_session.teacher.unavailable_slots:
            if (
                slot.day == new_session.timeslot.day and
                slot.start_time == new_session.timeslot.start_time
            ):
                print("Conflit : enseignant non disponible")
                return True
        return False
    def check_room_capacity(self, new_session):#constant 5:le nombre d'etudiant ne doit pas dépasser la capacité de la salle
        if new_session.room.capacity < new_session.groupe.effectif:
            print("Conflit : capacité salle insuffisante")
            return True
        return False
    
    def detect_conflict(self, new_session):
        checks = [
            self.check_room_conflict,
            self.check_teacher_conflict,
            self.check_group_conflict,
            self.check_teacher_availability,
            self.check_room_capacity,
        ]
        for check in checks:
            if check(new_session):
                return True
        return False

