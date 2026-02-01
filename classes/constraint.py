class ConstraintManager:
    def __init__(self, schedule):
        self.schedule = schedule
    
    def _is_same_slot(self, slot1, slot2):
        return slot1.day == slot2.day and slot1.start_time == slot2.start_time

    def check_capacity(self, room, student_count):
        return room.capacity >= student_count
    
    def check_teacher_availability(self, teacher, slot):
        if hasattr(teacher, 'unavailable_slots'):
            for bad_slot in teacher.unavailable_slots:
                if self._is_same_slot(bad_slot, slot):
                    return False
        return True
    
    def check_room_suitability(self, room, course):
        if course.students > room.capacity:
            return False

        if course.course_type == "TP" and room.room_type != "Lab":
            return False

        for item in course.needed_equipment:
            if item not in room.equipment:
                return False
        return True

    def check_teacher_workload(self, teacher):
        current_hours = 0
        for session in self.schedule.sessions:
            if session.teacher == teacher:

                current_hours += 2 
        
        return (current_hours + 2) <= teacher.max_hours

    def check_group_daily_limit(self, group_name, new_timeslot):
        daily_count = 0
        for session in self.schedule.sessions:
            if session.groupe == group_name and session.timeslot.day == new_timeslot.day:
                daily_count += 1
        
        return daily_count < 3

    def detect_conflicts(self, new_session):
        for existing in self.schedule.sessions:
            if self._is_same_slot(existing.timeslot, new_session.timeslot):
                if new_session.room == existing.room: return True
                if new_session.teacher == existing.teacher: return True
                if new_session.groupe == existing.groupe: return True
        return False