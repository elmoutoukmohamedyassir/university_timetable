class Schedule:
    def __init__(self):
        self.sessions = []

    def detect_conflict(self, new_session):
        for session in self.sessions:
            same_room = session.room == new_session.room
            same_day = session.timeslot.day == new_session.timeslot.day
            same_time = session.timeslot.start_time == new_session.timeslot.start_time

            same_teacher = session.teacher == new_session.teacher

            if (same_room and same_day and same_time) or (same_teacher and same_day and same_time):
                return True
        return False

    def add_session(self, session):
        if self.detect_conflict(session):
            print(" Conflict detected. Session not added.")
            return False
        self.sessions.append(session)

        print(" Session added successfully.")
        return True

    def display_schedule(self):
        for s in self.sessions:
            print(
                f"{s.course.name} ({s.course.course_type}) | "
                f"{s.timeslot.day} {s.timeslot.start_time}-{s.timeslot.end_time} | "
                f"Room: {s.room.name} | Teacher: {s.teacher.name}"
            )