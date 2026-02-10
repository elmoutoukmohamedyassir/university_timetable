import tkinter as tk
from tkinter import messagebox
from scheduler import Scheduler
from room import Room
from course import Course
from user import Admin, Teacher, Student

from student_gui import StudentDashboard
from teacher_gui import TeacherDashboard
from admin_gui import AdminDashboard

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Scheduler")
        self.root.geometry("900x600")

        self.scheduler = Scheduler()
        self.users = [] 
        
        self.requests = [
            {"id": 101, "teacher": "Prof. Smith", "room": "Room 1", "time": "Monday 08:30-10:20", "status": "Pending"}
        ]

        self.setup_scheduler()
        self.show_login_frame()

    def setup_scheduler(self):
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        times = ["08:30-10:20", "10:30-12:20", "14:30-16:20", "16:30-18:20"]
        
        self.scheduler.time_slots = [] 
        
        for day in days:
            for slot_time in times:
                self.scheduler.add_time_slot(f"{day} {slot_time}")

        
        self.scheduler.add_room(Room("Amphi A", 100, ["Projector"]))
        self.scheduler.add_room(Room("Salle 1", 30, ["Whiteboard"]))
        self.scheduler.add_room(Room("Salle 2", 30, ["Whiteboard", "Projector"]))
        self.scheduler.add_room(Room("Lab 1", 20, ["Projector"]))

        
        admin_user = Admin(1, "Admin User", "admin@school.edu")
        prof_smith = Teacher(2, "Prof. Smith", "smith@school.edu")
        student_doe = Student(3, "John Doe", "john@student.edu", "Group A")

        self.users = [admin_user, prof_smith, student_doe]

        
        self.scheduler.add_teacher(prof_smith)

        
        course_python = Course(101, "Python", "Lab", prof_smith, ["Group A"], 20, ["Projector"])
        self.scheduler.add_course(course_python)

    def show_login_frame(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=100)

        tk.Label(login_frame, text="University Scheduler Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(login_frame, text="Email").pack()
        self.email_entry = tk.Entry(login_frame)
        self.email_entry.pack(pady=5)

        tk.Label(login_frame, text="ID (Password)").pack()
        self.id_entry = tk.Entry(login_frame, show="*")
        self.id_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", command=self.verify_login).pack(pady=20)

    def verify_login(self):
        email = self.email_entry.get()
        user_id = self.id_entry.get()

        found_user = None
        for user in self.users:
            if user.email == email and str(user.id) == user_id:
                found_user = user
                break
        
        if found_user:
            self.current_user = found_user
            
            if isinstance(found_user, Admin):
                AdminDashboard(self.root, self.scheduler, self.users, self.requests, self.show_login_frame)
            
            elif isinstance(found_user, Teacher):
                TeacherDashboard(self.root, self.scheduler, self.current_user, self.requests, self.show_login_frame)
            
            elif isinstance(found_user, Student):
                StudentDashboard(self.root, self.scheduler, self.current_user, self.show_login_frame)
        else:
            messagebox.showerror("Error", "Invalid Email or ID")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()