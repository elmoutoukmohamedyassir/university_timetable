from classes.course import Course
from classes.room import Room
from classes.session import Session
from classes.major import Major
from classes.timeslot import TimeSlot
from classes.schedule import Schedule
from classes.constraint import ConstraintManager


def generate_timetables(majors, rooms, schedule):
    manager = ConstraintManager(schedule)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = ["08:00", "10:00", "14:00", "16:00"]
    
    all_slots = []
    for d in days:
        for h in hours:
            end_h = int(h.split(":")[0]) + 2
            end_time = f"{end_h:02d}:00" 
            all_slots.append(TimeSlot(d, h, end_time))

    for major in majors:
        # We assume all students in the major are "Group A" for this simplified version
        current_group = "Group A"

        for course in major.courses:
            is_scheduled = False
            
            for slot in all_slots:
                if is_scheduled: break

                # --- MANAGER CHECKS ---
                if not manager.check_teacher_availability(course.teacher, slot):
                    continue

                if not manager.check_teacher_workload(course.teacher):
                    continue

                if not manager.check_group_daily_limit(current_group, slot):
                    continue

                for room in rooms:
                    if not manager.check_room_suitability(room, course):
                        continue

                    new_session = Session(course, course.teacher, room, slot, current_group)

                    if manager.detect_conflicts(new_session):
                        continue
                    
                    # If we pass all checks, save it
                    schedule.add_session(new_session)
                    is_scheduled = True
                    break 
            
            if not is_scheduled:
                print(f"Could not find any slot for {course.name}")

if __name__ == "__main__":
    from classes.room import Room
    from classes.teacher import Teacher
    from classes.course import Course
    from classes.schedule import Schedule
    from classes.major import Major

    # 1. Setup Data
    r1 = Room("Room 101", 60, ["Projector"], room_type="Classroom") 
    r2 = Room("Gym", 100, ["Sound"], room_type="Amphitheater")
    r3 = Room("PC Lab 1", 30, ["PC"], room_type="Lab") 
    all_rooms = [r1, r2, r3]

    mr_smith = Teacher(1, "Mr. Smith", max_hours=4) 
    mrs_jones = Teacher(2, "Mrs. Jones")

    cs_major = Major("Computer Science")
    
    c1 = Course("Chemistry", "TP", 25)
    c1.teacher = mr_smith
    
    c2 = Course("Databases", "Lecture", 50)
    c2.teacher = mr_smith
    
    c3 = Course("Algorithms", "TD", 25) 
    c3.teacher = mrs_jones
    
    # Test Workload Limit: This 4th course should fail for Mr. Smith (Max 4 hours)
    c4 = Course("Python", "Lab", 25)
    c4.teacher = mr_smith 
    
    cs_major.courses = [c1, c2, c3, c4]

    # 2. Run
    my_schedule = Schedule()
    generate_timetables([cs_major], all_rooms, my_schedule)

    # 3. Result
    print("\n--- RESULT ---")
    my_schedule.display_schedule()