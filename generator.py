# Importing needed classes
from classes.course import Course
from classes.room import Room
from classes.session import Session
from classes.major import Major
from classes.timeslot import TimeSlot
from classes.schedule import Schedule

def generate_default_timeslots():
    slots =[]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [(8, 10), (10, 12), (14, 16), (16, 18)]

    for day in days:
        for start, end in hours:
                slots.append(TimeSlot(day, start, end))
    return slots

def get_capacity(room):
    return room.capacity

def generate_timetables(majors, rooms, my_schedule):
    all_slots = generate_default_timeslots()
    print('\n--- STARTING GENERATION ---')
    for major in majors:
        student_count = len(major.students)
        for course in major.courses:
             if not hasattr(course, 'teacher'):
                  print(f"Couldn't schedule the {course}")
                  continue
             is_scheduled = False
             for slot in all_slots:
                  if is_scheduled:
                       break
                  valid_rooms = []
                  for room in rooms:
                       if room.capacity >= student_count:
                            valid_rooms.append(room)
                  valid_rooms.sort(key=get_capacity)
                  for room in valid_rooms:
                      new_session = Session(course, course.teacher, room, slot)
                      new_session.major = major
                      if not my_schedule.detect_conflict(new_session):
                          my_schedule.add_session(new_session)
                          is_scheduled = True
                          break
                

# --- TEST BLOCK ---
if __name__ == "__main__":
    from teacher import Teacher
    from student import Student 
    # Ensure student.py is in the folder

    # 1. Create Rooms
    r1 = Room("Room 101", 30, ["Projector"]) 
    r2 = Room("Gym", 100, ["Sound"])
    all_rooms = [r1, r2]

    # 2. Create Teachers
    mr_smith = Teacher(1, "Mr. Smith")
    mrs_jones = Teacher(2, "Mrs. Jones")

    # 3. Create Major & Students
    cs_major = Major("Computer Science")
    # Add 25 fake students
    for i in range(25):
        # Adjust arguments if your Student class is different
        s = Student(i, f"Student_{i}", "CS", "Group A")
        cs_major.students.append(s)

    # 4. Create Courses (The Split Strategy)
    c1 = Course("Databases", "Lecture")
    c2 = Course("Databases", "TD")

    # 5. The "Sticky Note" Trick (Attach Teachers)
    c1.teacher = mr_smith
    c2.teacher = mrs_jones
    
    # Add to Major
    cs_major.courses = [c1, c2]

    # 6. Run Generator
    my_schedule = Schedule()
    generate_timetables([cs_major], all_rooms, my_schedule)

    # 7. Show Result
    print("\n--- FINAL TIMETABLE ---")
    my_schedule.display_schedule()
