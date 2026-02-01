from constraint_manager import ConstraintManager
class Schedule:
    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        if self.constraint_manager.detect_conflict(session):
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
