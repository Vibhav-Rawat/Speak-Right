from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from database import initialize_database
from auth import register, login
from practice import practice_session
from stats import (
    show_statistics,
    show_history,
    show_weak_words
)

console = Console()

def display_title():
    """Display the application title."""
    console.print(
        Panel.fit(
            "[bold cyan]Pronunciation Trainer[/bold cyan]",
            title="CS50 Python Final Project"
        )
    )


def get_main_menu_choice():
    """Ask the user to choose an option from the main menu."""
    return Prompt.ask(
        "\nSelect an option",
        choices=["1", "2", "3"]
    )


def get_dashboard_choice():
    """Ask the user to choose an option from the dashboard."""
    return Prompt.ask(
        "\nChoose an option",
        choices=["1", "2", "3", "4", "5"]
    )

def dashboard(user_id):
    """
    Displays the dashboard after a successful login.
    """

    while True:

        console.clear()

        console.print(
            Panel.fit(
                "[bold cyan]Dashboard[/bold cyan]",
                title="Pronunciation Trainer"
            )
        )

        console.print("[1] Practice")
        console.print("[2] Statistics")
        console.print("[3] History")
        console.print("[4] Weak Words")
        console.print("[5] Logout")

        choice = choice = get_dashboard_choice()

        if choice == "1":
            practice_session(user_id)

        elif choice == "2":
            show_statistics(user_id)

        elif choice == "3":
            show_history(user_id)

        elif choice == "4":
            show_weak_words(user_id)

        else:
            break


def main():

    initialize_database()

    while True:

        console.clear()

        console.print(
            Panel.fit(
                "[bold cyan]Pronunciation Trainer[/bold cyan]",
                title="CS50 Python Final Project"
            )
        )

        console.print("[1] Register")
        console.print("[2] Login")
        console.print("[3] Exit")

        choice = get_main_menu_choice()

        if choice == "1":
            register()

        elif choice == "2":

            user_id = login()

            if user_id:
                dashboard(user_id)

        else:
            console.print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()