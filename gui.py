# gui.py

import tkinter as tk
from export_utils import export_txt
from mock_data import edt

current_role = None  # global role variable


def open_timetable():
    window = tk.Toplevel()
    window.title("Timetable")

    tk.Label(
        window,
        text=f"Timetable view ({current_role})",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    text = tk.Text(window, width=80, height=20)
    text.pack(padx=10, pady=10)

    for session in edt:
        text.insert(
            tk.END,
            f"{session['day']} | {session['timeslot']} | "
            f"{session['course']} | {session['room']} | {session['teacher']}\n"
        )

    text.config(state=tk.DISABLED)


def main_menu():
    root = tk.Tk()
    root.title("Timetable Management System")

    tk.Label(
        root,
        text=f"Timetable Management System ({current_role})",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Button(
        root,
        text="Consult Timetable",
        width=25,
        command=open_timetable
    ).pack(pady=5)

    tk.Button(
        root,
        text="Export Timetable (TXT)",
        width=25,
        command=lambda: export_txt(edt)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Exit",
        width=25,
        command=root.destroy
    ).pack(pady=10)

    root.mainloop()


def choose_role(role_window):
    global current_role
    current_role = role_window
    role_selector.destroy()
    main_menu()


def role_selection():
    global role_selector
    role_selector = tk.Tk()
    role_selector.title("Select Role")

    tk.Label(
        role_selector,
        text="Select your role",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    tk.Button(
        role_selector,
        text="Student",
        width=20,
        command=lambda: choose_role("Student")
    ).pack(pady=5)

    tk.Button(
        role_selector,
        text="Teacher",
        width=20,
        command=lambda: choose_role("Teacher")
    ).pack(pady=5)

    role_selector.mainloop()
