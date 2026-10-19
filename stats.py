from rich.console import Console
from rich.table import Table

from database import (
    get_statistics,
    get_history,
    get_weak_words
)

console = Console()


def show_statistics(user_id):
    """
    Displays the user's overall statistics.
    """

    stats = get_statistics(user_id)

    total, average, highest, lowest = stats

    average = average if average is not None else 0
    highest = highest if highest is not None else 0
    lowest = lowest if lowest is not None else 0

    table = Table(title="Your Statistics")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Words Practiced", str(total))
    table.add_row("Average Score", f"{average:.2f}%")
    table.add_row("Highest Score", f"{highest:.2f}%")
    table.add_row("Lowest Score", f"{lowest:.2f}%")

    console.print(table)

    input("\nPress Enter to continue...")


def show_history(user_id):
    """
    Displays all previous pronunciation attempts.
    """

    history = get_history(user_id)

    table = Table(title="Practice History")

    table.add_column("Word")
    table.add_column("Score")
    table.add_column("Attempts")
    table.add_column("Date")

    for word, score, attempts, date in history:
        table.add_row(
            word,
            f"{score:.2f}%",
            str(attempts),
            date
        )

    console.print(table)

    input("\nPress Enter to continue...")


def show_weak_words(user_id):
    """
    Displays words with an average score below 70%.
    """

    weak_words = get_weak_words(user_id)

    table = Table(title="Words to Practice")

    table.add_column("Word")
    table.add_column("Average Score")

    for word, score in weak_words:
        table.add_row(word, f"{score:.2f}%")

    console.print(table)

    input("\nPress Enter to continue...")