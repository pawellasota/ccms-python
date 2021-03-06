import program
import ui
import menu


def main():
    """Method starts program and checks users access"""
    user_signed_in = None
    while not user_signed_in:
        user_signed_in = ui.Ui.get_login()
        if user_signed_in:
            print("Welcome "+user_signed_in.name)
            user_menu = menu.Menu.create_menu(user_signed_in)
            if user_menu == "exit":
                print("Logout successfully.")
                user_signed_in = True

        else:
            print("Wrong login input. Please try again.")


if __name__ == "__main__":
    main()