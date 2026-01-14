class ConstraintManager:
    def __init__(self, schedule):
          self.schedule = schedule
    def detect_conflict(self, new_session):
        for session in self.sessions:
            # 1. Calculate Time Overlaps
            same_day = session.timeslot.day == new_session.timeslot.day
            same_time = session.timeslot.start_time == new_session.timeslot.start_time
            
            # Optimization: If times are different, skip the rest!
            if not (same_day and same_time):
                continue
              
            # 2. Calculate Resource Overlaps
            same_room = session.room == new_session.room
            same_teacher = session.teacher == new_session.teacher # <--- MOVED UP!

            # 3. Check Major Conflict safely
            same_major = False
            if hasattr(session, 'major') and hasattr(new_session, 'major'):
                same_major = session.major == new_session.major

            # 4. Final Decision (One single IF statement)
            if same_room or same_teacher or same_major:
                return True

        return False
