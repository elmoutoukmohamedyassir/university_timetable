class Scheduler:
    def __init__(self):
        self.rooms = []
        self.teachers = []
        self.courses = []
        self.groups = []
        self.time_slots = []
    
    def add_room(self, room):
        self.rooms.append(room)

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_course(self, course):
        self.courses.append(course)

    def add_group(self, group):
        self.groups.append(group)
    
    def add_time_slot(self, slot):
        self.time_slots.append(slot)

    def check_room_availability(self, room_name, time_slot):
        for course in self.courses:
            if course.room is None:
                continue
            if course.room.name == room_name and course.time_slot == time_slot:
                return False
        return True
    
    def find_available_rooms(self, time_slot, min_capacity, needed_equipment):
        available_rooms = []
        
        for room in self.rooms:
            # 1. Check Capacity
            if room.capacity < min_capacity:
                continue
            
            if not set(needed_equipment).issubset(set(room.equipment)):
                continue

            if self.check_room_availability(room.name, time_slot):
                available_rooms.append(room)
        
        return available_rooms
    
    def check_teacher_availability(self, teacher_name, time_slot):
        for course in self.courses:
            if course.teacher.name == teacher_name and course.time_slot == time_slot:
                return False
        return True
    
    def check_group_availability(self, new_course_groups, time_slot):
        for course in self.courses:
            if course.time_slot == time_slot:
                if set(course.groups) & set(new_course_groups):
                    return False
        return True
    
    def check_capacity(self, room, course):
        return room.capacity >= course.attendees

    def check_equipment(self, room, course):
        return set(course.needed_equipment).issubset(set(room.equipment))
    
    def check_teacher_preferences(self, teacher, slot):
        if hasattr(teacher, 'unavailability') and slot in teacher.unavailability:
            return False
        
        if not teacher.availability:
            return True
        
        if slot in teacher.availability:
            return True
        
        return False

    def schedule_courses(self):
        for course in self.courses:
            if course.room is not None:
                continue
            for slot in self.time_slots:
                for room in self.rooms:
                    if (self.check_room_availability(room.name, slot) 
                        and 
                        self.check_teacher_availability(course.teacher.name, slot) 
                        and 
                        self.check_group_availability(course.groups, slot) 
                        and 
                        self.check_capacity(room, course) 
                        and 
                        self.check_equipment(room, course) 
                        and 
                        self.check_teacher_preferences(course.teacher, slot)):
                        course.room = room
                        course.time_slot = slot
                        break
                if course.room is not None:
                    break 
                
    def display_schedule(self):
        print("\n--- Final Course Schedule ---")
        scheduled_count = 0
        unscheduled_count = 0

        for course in self.courses:
            if course.room and course.time_slot:
                groups_str = ", ".join(course.groups) 
                print(f"Time: {course.time_slot:<15} | Course: {course.name:<10} | Room: {course.room.name:<10} | Teacher: {course.teacher.name} ({groups_str})")
                scheduled_count += 1
            else:
                print(f"WARNING: {course.name} could not be scheduled (Conflict or no slots).")
                unscheduled_count += 1
        
        print(f"\nSummary: {scheduled_count} scheduled, {unscheduled_count} failed.")