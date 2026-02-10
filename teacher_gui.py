import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class TeacherDashboard:
    def __init__(self, root, scheduler, current_user, requests_list, logout_callback):
        self.root = root
        self.scheduler = scheduler
        self.current_user = current_user
        self.requests = requests_list
        self.logout_callback = logout_callback
        
        self.show_teacher_dashboard()

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_teacher_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        sidebar = tk.Frame(self.root, width=200, bg="gray80", height=600, relief="sunken", borderwidth=1)
        sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

        tk.Label(sidebar, text=f"Welcome,\n{self.current_user.name}", bg="gray80", font=("Arial", 12, "bold")).pack(pady=20)

        tk.Button(sidebar, text="My Schedule", width=20, command=self.view_teacher_schedule).pack(pady=10)
        tk.Button(sidebar, text="Search Rooms", width=20, command=self.open_search_room_window).pack(pady=10)
        tk.Button(sidebar, text="Request Room", width=20, command=self.open_request_room_window).pack(pady=10)
        tk.Button(sidebar, text="Report Absence", width=20, command=self.open_unavailability_window).pack(pady=10)
        # Note: Reusing export logic if needed, or simply remove if not strictly required by your original code
        tk.Button(sidebar, text="Logout", width=20, command=self.logout_callback, fg="red").pack(pady=30)

        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(expand=True, fill="both", side="right")
        
        self.view_teacher_schedule()

    def view_teacher_schedule(self):
        self.clear_content()
        tk.Label(self.main_content, text=f"Schedule for {self.current_user.name}", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        columns = ("Time", "Course", "Room", "Group")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        tree.pack(expand=True, fill="both", padx=20, pady=10)
        
        for course in self.scheduler.courses:
            if course.teacher.email == self.current_user.email:
                if course.room and course.time_slot:
                    tree.insert("", "end", values=(course.time_slot, course.name, course.room.name, ", ".join(course.groups)))

    def open_request_room_window(self):
        self.req_popup = tk.Toplevel(self.root)
        self.req_popup.title("Request a Room")
        self.req_popup.geometry("300x250")

        tk.Label(self.req_popup, text="Select Room:").pack(pady=5)

        room_names = [r.name for r in self.scheduler.rooms]
        self.combo_room = ttk.Combobox(self.req_popup, values=room_names)
        self.combo_room.pack(pady=5)

        tk.Label(self.req_popup, text="Desired Time Slot:").pack(pady=5)

        self.combo_time = ttk.Combobox(self.req_popup, values=self.scheduler.time_slots)
        self.combo_time.pack(pady=5)

        tk.Label(self.req_popup, text="Group (e.g., Group A):").pack(pady=5)
        self.entry_group = tk.Entry(self.req_popup)
        self.entry_group.pack(pady=5)

        tk.Label(self.req_popup, text="Reason (ex: Rattrapage):").pack(pady=5)
        self.entry_reason = tk.Entry(self.req_popup)
        self.entry_reason.pack(pady=5)

        tk.Button(self.req_popup, text="Submit Request", command=self.submit_room_request, bg="blue", fg="white").pack(pady=20)

    def submit_room_request(self):
        room = self.combo_room.get()
        time = self.combo_time.get()
        group = self.entry_group.get()
        reason = self.entry_reason.get()
    
        if room and time and reason:
            new_id = len(self.requests) + 101
            
            new_request = {
                "id": new_id,
                "teacher": self.current_user.name,
                "room": room,
                "time": time,
                "group": group,
                "reason": reason,
                "status": "Pending"
            }
            
            self.requests.append(new_request)
            messagebox.showinfo("Success", "Request submitted to Admin!")
            self.req_popup.destroy()
        else:
            messagebox.showwarning("Error", "Please fill all fields (Room, Time, and Reason)")

    def open_unavailability_window(self):
        self.abs_popup = tk.Toplevel(self.root)
        self.abs_popup.title("Report Unavailability")
        self.abs_popup.geometry("300x200")

        tk.Label(self.abs_popup, text="Select Time Slot to Block:", font=("Arial", 10, "bold")).pack(pady=10)

        self.combo_abs_time = ttk.Combobox(self.abs_popup, values=self.scheduler.time_slots)
        self.combo_abs_time.pack(pady=5)

        tk.Label(self.abs_popup, text="This will unschedule any existing\nclasses in this slot.", fg="red", font=("Arial", 9)).pack(pady=10)

        tk.Button(self.abs_popup, text="Confirm Unavailability", command=self.submit_unavailability, bg="red", fg="white").pack(pady=10)

    def submit_unavailability(self):
        slot = self.combo_abs_time.get()
        
        if not slot:
            messagebox.showwarning("Error", "Please select a time slot.")
            return

        if slot not in self.current_user.unavailability:
            self.current_user.unavailability.append(slot)
        else:
            messagebox.showinfo("Info", "You already marked this slot as unavailable.")
            return

        conflict_found = False
        for course in self.scheduler.courses:
            if course.teacher.email == self.current_user.email and course.time_slot == slot:
                course.room = None
                course.time_slot = None
                conflict_found = True
                print(f"Readjustment: {course.name} has been unscheduled.")

        if conflict_found:
            messagebox.showinfo("Readjustment", f"Unavailability recorded.\n\nCONFLICT FOUND: Your class in this slot has been unscheduled.\nPlease contact Admin to reschedule.")
        else:
            messagebox.showinfo("Success", "Unavailability recorded. No scheduling conflicts found.")
            
        self.abs_popup.destroy()
        self.view_teacher_schedule()

    def open_search_room_window(self):
        self.search_popup = tk.Toplevel(self.root)
        self.search_popup.title("Find a Vacant Room")
        self.search_popup.geometry("400x500")

        tk.Label(self.search_popup, text="Search Criteria", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.search_popup, text="Time Slot:").pack()
        self.search_time = ttk.Combobox(self.search_popup, values=self.scheduler.time_slots)
        self.search_time.pack(pady=5)

        tk.Label(self.search_popup, text="Minimum Capacity:").pack()
        self.search_capacity = tk.Spinbox(self.search_popup, from_=1, to=100)
        self.search_capacity.pack(pady=5)

        tk.Label(self.search_popup, text="Required Equipment:").pack(pady=5)
        
        self.var_projector = tk.BooleanVar()
        self.var_whiteboard = tk.BooleanVar()
        
        tk.Checkbutton(self.search_popup, text="Projector", variable=self.var_projector).pack()
        tk.Checkbutton(self.search_popup, text="Whiteboard", variable=self.var_whiteboard).pack()

        tk.Button(self.search_popup, text="Search", command=self.perform_room_search, bg="blue", fg="white").pack(pady=15)

        tk.Label(self.search_popup, text="Available Rooms:").pack()
        self.results_list = tk.Listbox(self.search_popup, height=6)
        self.results_list.pack(pady=5, fill="x", padx=20)

    def perform_room_search(self):
        time = self.search_time.get()
        try:
            capacity = int(self.search_capacity.get())
        except ValueError:
            capacity = 0
            
        equipment = []
        if self.var_projector.get(): equipment.append("Projector")
        if self.var_whiteboard.get(): equipment.append("Whiteboard")

        if not time:
            messagebox.showwarning("Error", "Please select a time slot.")
            return

        rooms = self.scheduler.find_available_rooms(time, capacity, equipment)

        self.results_list.delete(0, tk.END)
        
        if rooms:
            for room in rooms:
                self.results_list.insert(tk.END, f"{room.name} (Cap: {room.capacity}, Eq: {', '.join(room.equipment)})")
        else:
            self.results_list.insert(tk.END, "No rooms match these criteria.")