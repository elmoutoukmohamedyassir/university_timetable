# export_utils.py

def export_txt(edt, filename="exports/timetable.txt"):
    with open(filename, "w") as file:
        file.write("DAY | TIMESLOT | COURSE | ROOM | TEACHER\n")
        file.write("-" * 40 + "\n")
        for session in edt:
            file.write(
                f"{session['day']} | {session['timeslot']} | "
                f"{session['course']} | {session['room']} | {session['teacher']}\n"
            )

    print(f"\nTimetable exported successfully to {filename} ")
