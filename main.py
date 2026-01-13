from room import Room
from course import Course
from timeslot import TimeSlot
from teacher import Teacher
from session import Session
from schedule import Schedule

# Create objects
room1 = Room("Room A", 40, ["Projector"])
teacher1 = Teacher(1, "saad eddine abarra")
course1 = Course("Databases", "Lecture")
timeslot1 = TimeSlot("Monday", 8, 10)

# Create session
session1 = Session(course1, teacher1, room1, timeslot1)

# Schedule
schedule = Schedule()
schedule.add_session(session1)
schedule.display_schedule()
