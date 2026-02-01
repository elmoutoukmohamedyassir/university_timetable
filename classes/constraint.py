class ConstraintManager:
    def __init__(self, schedule):
        self.schedule = schedule
    
    def _is_same_slot(self, slot1, slot2):
        if (slot1.day == slot2.day and slot1.start_time == slot2.start_time):
            return True
        else:
            return False

    def check_capacity(self, room, student_count):
        if (room.capacity >= student_count):
            return True
        else:
            return False
    
    def check_teacher_availability(self, teacher, slot):
        for bad_slot in teacher.unavailable_slots:
            if self._is_same_slot(bad_slot, slot):
                return False
        return True
    
    def check_room_suitability(self, room, course):
        # TP constraint
        if course.course_type == "TP":
            if room.room_type != "Lab":
                return False

        # Equipment constraint
        for item in course.needed_equipment:
            if item not in room.equipment:
                return False
        
        return True

    def check_teacher_workload(self, teacher):
        current_hours = 0
        for session in self.schedule.sessions:
            if session.teacher == teacher:
                duration = session.timeslot.end_time - session.timeslot.start_time
                current_hours += duration
        if current_hours + 2 > teacher.max_hours:
            return False
            
        return True

    def check_group_daily_limit(self, major, new_timeslot):
        daily_count = 0
        target_day = new_timeslot.day

        for session in self.schedule.sessions:
            if session.major == major:
                if session.timeslot.day == target_day:
                    daily_count += 1
                    
        if daily_count >= 3:
            return False
            
        return True

    def detect_conflicts(self, new_session):
        for existing_session in self.schedule.sessions:
            if self._is_same_slot(existing_session.timeslot, new_session.timeslot):
                if new_session.room == existing_session.room: return True
                if new_session.teacher == existing_session.teacher: return True
                if new_session.groupe == existing_session.groupe: return True
        return False

