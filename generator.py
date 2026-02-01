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
    hours = [(8, 10), (10, 12), (14, 16), (16, 18)]

    for day in days:
        for start, end in hours:
            slots.append(TimeSlot(day, start, end))
    return slots

def get_capacity(room):
    return room.capacity

def generate_timetables(majors, rooms, my_schedule):
    pass
