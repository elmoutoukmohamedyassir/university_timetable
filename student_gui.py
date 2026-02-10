import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class StudentDashboard:
    def __init__(self, root, scheduler, current_user, logout_callback):
        self.root = root
        self.scheduler = scheduler
        self.current_user = current_user
        self.logout_callback = logout_callback
        
        # Start the dashboard immediately
        self.show_student_dashboard()

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_student_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        sidebar = tk.Frame(self.root, width=200, bg="gray80", height=600, relief="sunken", borderwidth=1)
        sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

        tk.Label(sidebar, text=f"Student Space", bg="gray80", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(sidebar, text=f"{self.current_user.name}", bg="gray80", font=("Arial", 11)).pack()
        tk.Label(sidebar, text=f"Group: {self.current_user.group}", bg="gray80", fg="blue", font=("Arial", 10, "bold")).pack(pady=5)

        tk.Button(sidebar, text="My Schedule", width=20, command=self.view_student_schedule, bg="white").pack(pady=10)
        tk.Button(sidebar, text="Find Empty Room", width=20, command=self.open_search_room_window, bg="white").pack(pady=10)
        tk.Button(sidebar, text="Download Schedule", width=20, command=self.export_student_schedule, bg="#eee").pack(pady=10)
        
        tk.Button(sidebar, text="Logout", width=20, command=self.logout_callback, fg="red").pack(pady=30)

        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(expand=True, fill="both", side="right")

        self.view_student_schedule()

    def view_student_schedule(self):
        self.clear_content()
        header_frame = tk.Frame(self.main_content, bg="white")
        header_frame.pack(fill="x", pady=20, padx=20)
        
        tk.Label(header_frame, text=f"Weekly Schedule: {self.current_user.group}", font=("Arial", 18, "bold"), bg="white").pack(side="left")
        
        tk.Button(header_frame, text="↻ Refresh Updates", command=self.view_student_schedule, bg="#ddd").pack(side="right")

        columns = ("Time Slot", "Course Name", "Room", "Teacher")
        tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        
        tree.pack(expand=True, fill="both", padx=20, pady=10)

        found_courses = False
        for course in self.scheduler.courses:
            if self.current_user.group in course.groups:
                if course.room and course.time_slot:
                    tree.insert("", "end", values=(
                        course.time_slot, 
                        course.name, 
                        course.room.name, 
                        course.teacher.name
                    ))
                    found_courses = True
                else:
                    tree.insert("", "end", values=(
                        "TBD", 
                        course.name, 
                        "Not Assigned", 
                        course.teacher.name
                    ))

        if not found_courses:
            tk.Label(self.main_content, text="No classes scheduled for this group yet.", fg="gray", bg="white").pack()

    def export_student_schedule(self):
        filename = filedialog.asksaveasfilename(
            title="Save My Schedule",
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if not filename: return

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Time Slot", "Course", "Room", "Teacher"])

                for course in self.scheduler.courses:
                    if self.current_user.group in course.groups and course.room:
                        writer.writerow([
                            course.time_slot,
                            course.name,
                            course.room.name,
                            course.teacher.name
                        ])
            messagebox.showinfo("Success", "Your schedule has been downloaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

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