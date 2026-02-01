# interface.py

from mock_data import edt


def show_edt():
    print("\n------ TIMETABLE ------")
    for session in edt:
        print(
            f"{session['day']} | {session['timeslot']} | "
            f"{session['course']} | {session['room']} | {session['teacher']}"
        )


def reservation_request():
    print("\n--- Reservation Request ---")
    course = input("Course name: ")
    day = input("Day: ")
    time = input("Time: ")

    print("\nReservation request sent successfully ")
    print(f"Course: {course}, Day: {day}, Time: {time}")


def menu(role):
    while True:
        print("\n===== MENU =====")
        print("1. Consult timetable")
        print("2. Request reservation")
        print("3. Logout")

        choice = input("Your choice: ")

        if choice == "1":
            show_edt()
        elif choice == "2":
            reservation_request()
        elif choice == "3":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    role = "student"  # you can change this if needed
    menu(role)
