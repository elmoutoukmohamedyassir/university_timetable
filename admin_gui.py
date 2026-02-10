import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from room import Room
from course import Course
from user import Teacher, Student

class AdminDashboard:
    def __init__(self, root, scheduler, users_list, requests_list, logout_callback):
        self.root = root
        self.scheduler = scheduler
        self.users = users_list
        self.requests = requests_list
        self.logout_callback = logout_callback
        
        self.show_admin_dashboard()

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_admin_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        sidebar = tk.Frame(self.root, width=200, bg="gray80", height=600, relief="sunken", borderwidth=1)
        sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

        tk.Label(sidebar, text="Admin Menu", bg="gray80", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(sidebar, text="Manage Rooms", width=20, command=self.view_manage_rooms).pack(pady=10)
        tk.Button(sidebar, text="Manage Teachers", width=20, command=self.view_manage_teachers).pack(pady=10)
        tk.Button(sidebar, text="Manage Students", width=20, command=self.view_manage_students).pack(pady=10)
        tk.Button(sidebar, text="Manage Courses", width=20, command=self.view_manage_courses).pack(pady=10) # Using existing method name or linking to logic
        tk.Button(sidebar, text="Generate Timetables", width=20, command=self.run_scheduler).pack(pady=10)
        tk.Button(sidebar, text="Room Requests", width=20, command=self.view_room_requests).pack(pady=10)
        tk.Button(sidebar, text="Statistics", width=20, command=self.view_statistics).pack(pady=10)
        tk.Button(sidebar, text="Export Schedule", width=20, command=self.export_schedule).pack(pady=10)
        tk.Button(sidebar, text="Logout", width=20, command=self.logout_callback, fg="red").pack(pady=30)

        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(expand=True, fill="both", side="right")

        tk.Label(self.main_content, text="Welcome Admin", font=("Arial", 20), bg="white").pack(pady=50)

    def view_manage_teachers(self):
        self.clear_content()
        tk.Label(self.main_content, text="Manage Teachers", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        tk.Button(self.main_content, text="+ Add New Teacher", bg="green", fg="white", command=self.open_add_teacher_window).pack(pady=10)

        columns = ("ID", "Name", "Email", "Availability")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
            
        tree.pack(expand=True, fill="both", padx=20, pady=10)

        for teacher in self.scheduler.teachers:
            avail_str = ", ".join(teacher.availability) if teacher.availability else "All"
            tree.insert("", "end", values=(teacher.id, teacher.name, teacher.email, avail_str))

    def open_add_teacher_window(self):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Add Teacher")
        self.popup.geometry("300x250")

        tk.Label(self.popup, text="Name:").pack(pady=5)
        self.entry_name = tk.Entry(self.popup)
        self.entry_name.pack(pady=5)

        tk.Label(self.popup, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.popup)
        self.entry_email.pack(pady=5)

        tk.Label(self.popup, text="ID (Password):").pack(pady=5)
        self.entry_id = tk.Entry(self.popup)
        self.entry_id.pack(pady=5)

        tk.Button(self.popup, text="Save", command=self.save_new_teacher, bg="blue", fg="white").pack(pady=20)

    def save_new_teacher(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        t_id = self.entry_id.get()

        if name and email and t_id:
            new_teacher = Teacher(int(t_id), name, email)
            self.scheduler.add_teacher(new_teacher)
            self.users.append(new_teacher)
            messagebox.showinfo("Success", f"{name} added successfully!")
            self.popup.destroy()
            self.view_manage_teachers()
        else:
            messagebox.showwarning("Error", "Please fill all fields")

    def view_room_requests(self):
        self.clear_content()
        tk.Label(self.main_content, text="Pending Room Requests", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        columns = ("Request ID", "Teacher", "Room Requested", "Time Slot", "Group", "Reason", "Status")
        self.req_tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.req_tree.heading(col, text=col)
            self.req_tree.column(col, anchor="center", width=100)

        self.req_tree.pack(expand=True, fill="x", padx=20, pady=10)

        for req in self.requests:
            if req["status"] == "Pending":
                self.req_tree.insert("", "end", values=(
                    req["id"], 
                    req["teacher"], 
                    req["room"], 
                    req["time"],
                    req.get("group", "N/A"),
                    req.get("reason", "N/A"),
                    req["status"]
                ))

        btn_frame = tk.Frame(self.main_content, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Approve Selected", bg="green", fg="white", command=self.approve_request).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Reject Selected", bg="red", fg="white", command=self.reject_request).pack(side="left", padx=10)

    def approve_request(self):
        selected = self.req_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request to approve.")
            return
        
        item = self.req_tree.item(selected)
        req_id = item['values'][0]
        
        for req in self.requests:
            if req["id"] == req_id:
                if req["status"] == "Approved":
                    messagebox.showinfo("Info", "This request is already approved.")
                    return

                req["status"] = "Approved"
                
                room_obj = next((r for r in self.scheduler.rooms if r.name == req["room"]), None)
                teacher_obj = next((t for t in self.scheduler.teachers if t.name == req["teacher"]), None)
                
                target_group = req.get("group", "")
                
                if room_obj and teacher_obj:
                    reservation = Course(
                        id=9000 + req["id"],
                        name=req.get("reason", "Reservation"), 
                        type="Reservation",
                        teacher=teacher_obj,
                        groups=[target_group],
                        attendees=0,
                        needed_equipment=[]
                    )
                    reservation.room = room_obj
                    reservation.time_slot = req["time"]
                    
                    self.scheduler.add_course(reservation)
                    
                    messagebox.showinfo("Success", f"Approved!\nAdded '{req.get('reason')}' for Group {target_group}.")
                else:
                    messagebox.showerror("Error", "Could not find Room or Teacher object.")
                
                break
        self.view_room_requests()

    def reject_request(self):
        selected = self.req_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request to reject.")
            return
        item = self.req_tree.item(selected)
        req_id = item['values'][0]
        for req in self.requests:
            if req["id"] == req_id:
                req["status"] = "Rejected"
                messagebox.showinfo("Rejected", f"Request for {req['teacher']} rejected.")
                break
        self.view_room_requests()

    def view_manage_rooms(self):
        self.clear_content()
        tk.Label(self.main_content, text="Manage Rooms", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Button(self.main_content, text="+ Add New Room", bg="green", fg="white", command=self.open_add_room_window).pack(pady=10)

        columns = ("Name", "Capacity", "Equipment")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        
        tree.pack(padx=20, pady=10, fill="x")

        for room in self.scheduler.rooms:
            equip_str = ", ".join(room.equipment)
            tree.insert("", "end", values=(room.name, room.capacity, equip_str))

    def open_add_room_window(self):
        self.room_popup = tk.Toplevel(self.root)
        self.room_popup.title("Add Room")
        self.room_popup.geometry("300x300")

        tk.Label(self.room_popup, text="Room Name:").pack(pady=5)
        self.entry_room_name = tk.Entry(self.room_popup)
        self.entry_room_name.pack(pady=5)

        tk.Label(self.room_popup, text="Capacity:").pack(pady=5)
        self.spin_capacity = tk.Spinbox(self.room_popup, from_=1, to=500)
        self.spin_capacity.pack(pady=5)

        tk.Label(self.room_popup, text="Equipment:").pack(pady=5)
        self.var_proj = tk.BooleanVar()
        self.var_board = tk.BooleanVar()
        tk.Checkbutton(self.room_popup, text="Projector", variable=self.var_proj).pack()
        tk.Checkbutton(self.room_popup, text="Whiteboard", variable=self.var_board).pack()

        tk.Button(self.room_popup, text="Save Room", command=self.save_new_room, bg="blue", fg="white").pack(pady=20)

    def save_new_room(self):
        name = self.entry_room_name.get()
        try:
            cap = int(self.spin_capacity.get())
        except ValueError:
            cap = 0
        
        equip = []
        if self.var_proj.get(): equip.append("Projector")
        if self.var_board.get(): equip.append("Whiteboard")

        if name and cap > 0:
            new_room = Room(name, cap, equip)
            self.scheduler.add_room(new_room)
            
            messagebox.showinfo("Success", f"Room '{name}' added!")
            self.room_popup.destroy()
            self.view_manage_rooms()
        else:
            messagebox.showwarning("Error", "Please enter a valid Name and Capacity")

    def view_manage_students(self):
        self.clear_content()
        tk.Label(self.main_content, text="Manage Students", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Button(self.main_content, text="+ Add New Student", bg="green", fg="white", command=self.open_add_student_window).pack(pady=10)

        
        columns = ("ID", "Name", "Email", "Group")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        
        tree.pack(padx=20, pady=10, fill="x")

        
        for user in self.users:
            if isinstance(user, Student):
                tree.insert("", "end", values=(user.id, user.name, user.email, user.group))

    def open_add_student_window(self):
        self.student_popup = tk.Toplevel(self.root)
        self.student_popup.title("Add Student")
        self.student_popup.geometry("300x300")

        tk.Label(self.student_popup, text="Student Name:").pack(pady=5)
        self.entry_s_name = tk.Entry(self.student_popup)
        self.entry_s_name.pack(pady=5)

        tk.Label(self.student_popup, text="Email:").pack(pady=5)
        self.entry_s_email = tk.Entry(self.student_popup)
        self.entry_s_email.pack(pady=5)

        tk.Label(self.student_popup, text="Group (e.g. Group A):").pack(pady=5)
        self.entry_s_group = tk.Entry(self.student_popup)
        self.entry_s_group.pack(pady=5)

        tk.Button(self.student_popup, text="Save Student", command=self.save_new_student, bg="blue", fg="white").pack(pady=20)

    def save_new_student(self):
        name = self.entry_s_name.get()
        email = self.entry_s_email.get()
        group = self.entry_s_group.get()

        if name and email and group:
            new_id = len(self.users) + 1
            new_student = Student(new_id, name, email, group)
            self.users.append(new_student)
            messagebox.showinfo("Success", f"Student Added!\nID (Password): {new_id}")
            self.student_popup.destroy()
            self.view_manage_students()
        else:
            messagebox.showwarning("Error", "Please fill all fields")

    def view_manage_courses(self):
        self.clear_content()
        tk.Label(self.main_content, text="Manage Courses", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Button(self.main_content, text="+ Add New Course", bg="green", fg="white", command=self.open_add_course_window).pack(pady=10)

        columns = ("ID", "Name", "Teacher", "Groups")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(padx=20, pady=10, fill="x")

        for c in self.scheduler.courses:
            tree.insert("", "end", values=(c.id, c.name, c.teacher.name, ", ".join(c.groups)))

    def open_add_course_window(self):
        self.course_popup = tk.Toplevel(self.root)
        self.course_popup.title("Add Course")
        self.course_popup.geometry("350x450")

        tk.Label(self.course_popup, text="Course Name:").pack(pady=2)
        self.entry_c_name = tk.Entry(self.course_popup)
        self.entry_c_name.pack(pady=2)

        tk.Label(self.course_popup, text="Type (Lecture/Lab):").pack(pady=2)
        self.combo_c_type = ttk.Combobox(self.course_popup, values=["Lecture", "Lab", "TD"])
        self.combo_c_type.pack(pady=2)

        tk.Label(self.course_popup, text="Select Teacher:").pack(pady=2)
        teacher_names = [t.name for t in self.scheduler.teachers]
        self.combo_c_teacher = ttk.Combobox(self.course_popup, values=teacher_names)
        self.combo_c_teacher.pack(pady=2)

        tk.Label(self.course_popup, text="Groups (comma separated):").pack(pady=2)
        self.entry_c_groups = tk.Entry(self.course_popup)
        self.entry_c_groups.pack(pady=2)

        tk.Label(self.course_popup, text="Estimated Attendees:").pack(pady=2)
        self.spin_c_attendees = tk.Spinbox(self.course_popup, from_=1, to=200)
        self.spin_c_attendees.pack(pady=2)

        tk.Label(self.course_popup, text="Needed Equipment:").pack(pady=5)
        self.var_c_proj = tk.BooleanVar()
        self.var_c_board = tk.BooleanVar()
        tk.Checkbutton(self.course_popup, text="Projector", variable=self.var_c_proj).pack()
        tk.Checkbutton(self.course_popup, text="Whiteboard", variable=self.var_c_board).pack()

        tk.Button(self.course_popup, text="Save Course", command=self.save_new_course, bg="blue", fg="white").pack(pady=20)

    def save_new_course(self):
        name = self.entry_c_name.get()
        c_type = self.combo_c_type.get()
        t_name = self.combo_c_teacher.get()
        groups_str = self.entry_c_groups.get()
        
        if not (name and t_name and groups_str):
            messagebox.showwarning("Error", "Please fill Name, Teacher, and Groups.")
            return

        selected_teacher = None
        for t in self.scheduler.teachers:
            if t.name == t_name:
                selected_teacher = t
                break
        
        if not selected_teacher:
            messagebox.showerror("Error", "Teacher not found! Please add them in 'Manage Teachers' first.")
            return

        groups_list = [g.strip() for g in groups_str.split(",")]
        try:
            attendees = int(self.spin_c_attendees.get())
        except ValueError:
            attendees = 0
        
        equip = []
        if self.var_c_proj.get(): equip.append("Projector")
        if self.var_c_board.get(): equip.append("Whiteboard")

        new_id = len(self.scheduler.courses) + 101
        
        new_course = Course(new_id, name, c_type, selected_teacher, groups_list, attendees, equip)
        self.scheduler.add_course(new_course)
        
        messagebox.showinfo("Success", "Course Added Successfully!")
        self.course_popup.destroy()
        self.view_manage_courses()

    def run_scheduler(self):
        self.scheduler.schedule_courses()
        self.view_schedule()
        messagebox.showinfo("Success", "Schedule Generated Successfully!")

    def view_schedule(self):
        self.clear_content()
        tk.Label(self.main_content, text="Generated Schedule", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        columns = ("Time", "Course", "Room", "Teacher", "Group")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(expand=True, fill="both", padx=20, pady=10)

        for course in self.scheduler.courses:
            if course.room and course.time_slot:
                tree.insert("", "end", values=(course.time_slot, course.name, course.room.name, course.teacher.name, ", ".join(course.groups)))
            else:
                tree.insert("", "end", values=("UNSCHEDULED", course.name, "N/A", course.teacher.name, "Conflict"))

    def view_statistics(self):
        self.clear_content()
        
        tk.Label(self.main_content, text="System Statistics", font=("Arial", 20, "bold"), bg="white", fg="black").pack(pady=20)
        
        total_courses = len(self.scheduler.courses)
        
        scheduled_courses = 0
        for c in self.scheduler.courses:
            if c.room and c.time_slot:
                scheduled_courses += 1
                
        unscheduled = total_courses - scheduled_courses
        
        total_rooms = len(self.scheduler.rooms)
        total_teachers = len(self.scheduler.teachers)
        total_students = len([u for u in self.users if isinstance(u, Student)])

        stats_text = (
            f"Total Courses:      {total_courses}\n"
            f"   • Scheduled:     {scheduled_courses}\n"
            f"   • Unscheduled:   {unscheduled}\n\n"
            f"Total Teachers:     {total_teachers}\n"
            f"Total Students:     {total_students}\n"
            f"Total Rooms:        {total_rooms}"
        )
        
        stat_frame = tk.Frame(self.main_content, bg="white", relief="groove", bd=2)
        stat_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(stat_frame, text=stats_text, font=("Courier", 14), justify="left", bg="white", fg="black").pack(pady=20, padx=20)

    def export_schedule(self):
        filename = filedialog.asksaveasfilename(
            initialdir=".",
            title="Export Schedule to Excel/CSV",
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if not filename:
            return
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Time Slot", "Course Name", "Type", "Room", "Teacher", "Groups"])           
                count = 0
                for course in self.scheduler.courses:
                    if course.room and course.time_slot:
                        writer.writerow([
                            course.time_slot,
                            course.name,
                            course.type,
                            course.room.name,
                            course.teacher.name,
                            ", ".join(course.groups)
                        ])
                        count += 1
            
            messagebox.showinfo("Export Successful", f"Successfully exported {count} courses to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save file:\n{str(e)}")