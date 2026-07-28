from menu import print_menu
from candidates import create_candidates_table
from notifications import create_notifications_table
from task import (
    add_candidate,
    show_candidates,
    search_candidate,
    update_candidate,
    delete_candidate
)

from crawler import crawl_jntuh_notifications


def main():

    # Create database tables when application starts
    create_candidates_table()
    create_notifications_table()

    while True:

        print_menu()

        option = input("Enter an option: ")

        if option == "1":

            add_candidate()

        elif option == "2":

            show_candidates()

        elif option == "3":

            search_candidate()

        elif option == "4":

            update_candidate()

        elif option == "5":

            delete_candidate()

        elif option == "6":

            crawl_jntuh_notifications()

        elif option == "7":

            print("\nThank you for using JRF_NET.")
            print("Exiting application...")

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select a valid option."
            )


if __name__ == "__main__":
    main()