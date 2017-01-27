import program
import ui
import menu


def main():
    """Method starts program and checks users access"""
    codecool = program.Program("csv_lists/employee_list.csv",
                               "csv_lists/students_list.csv",
                               "csv_lists/mentors_list.csv",
                               "csv_lists/managers_list.csv",
                               "csv_lists/assignments_list.csv",
                               "csv_lists/submissions_list.csv",
                               "csv_lists/attendance_list.csv"
                               )

    user_signed_in = None
    while not user_signed_in:
        user_signed_in = ui.Ui.get_login(codecool)
        if user_signed_in:
            print("Welcome "+user_signed_in.name)
            user_menu = menu.Menu.create_menu(user_signed_in, codecool)
            if user_menu == "exit":
                codecool.export_data()
                print("Logout successfully.")
                user_signed_in = None
                continue
        else:
            print("Wrong login input. Please try again.")


if __name__ == "__main__":
    main()