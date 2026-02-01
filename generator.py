from classes.course import Course
from classes.room import Room
from classes.session import Session
from classes.major import Major
from classes.timeslot import TimeSlot
from classes.schedule import Schedule
from classes.constraint import ConstraintManager

def generate_default_timeslots():
    slots = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [
        (8.0, 9.5),    # 08:00 - 09:30
        (9.75, 11.25), # 09:45 - 11:15 (Break was 9:30-9:45)
        (11.5, 13.0),  # 11:30 - 13:00 (Break was 11:15-11:30)
        (14.0, 15.5),  # 14:00 - 15:30 (Lunch break 13:00-14:00)
        (15.75, 17.25) # 15:45 - 17:15 (Break was 15:30-15:45)
    ]

    for day in days:
        for start, end in hours:
            slots.append(TimeSlot(day, start, end))
    return slots

def get_capacity(room):
    return room.capacity

def generate_timetables(majors, rooms, my_schedule):
    manager = ConstraintManager(my_schedule)
    all_slots = generate_default_timeslots()

    for major in majors:
        for course in major.courses:
            
            is_scheduled = False 
            
            student_count = len(major.students)

            for slot in all_slots:
                
                if is_scheduled: 
                    break 

                if not manager.check_teacher_availability(course.teacher, slot):
                    continue

                if not manager.check_teacher_workload(course.teacher):
                    continue

                if not manager.check_group_daily_limit(major, slot):
                    continue

                for room in rooms:
                    if not manager.check_capacity(room, student_count):
                        continue

                    if not manager.check_room_suitability(room, course):
                        continue 
                
                    new_session = Session(course, course.teacher, room, slot, major)

                    if not manager.detect_conflicts(new_session):
                        my_schedule.add_session(new_session)
                        course.teacher.add_unavailability(slot)
                        
                        is_scheduled = True
                        break 

            if not is_scheduled:
                print(f"Could not find a slot for {course.name}")