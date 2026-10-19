import os
import tempfile

from rich.console import Console
from rich.prompt import Prompt

from speech import speak, record_audio, generate_reference, verify_word
from utils import compare_audio, get_performance, format_score, word_matches
from database import get_random_word, save_attempt

console = Console()

DIFFICULTY_MAP = {
    "1": "Beginner",
    "2": "Intermediate",
    "3": "Advanced"
}


def score_attempt(word, ref_path, user_path):
    score = compare_audio(ref_path, user_path)
    spoken_word = verify_word(user_path)

    print(f"Target word: {word}")
    print(f"Recognized word: {spoken_word}")
    print(f"Audio similarity: {score}")

    if spoken_word is None:
        return None

    if not word_matches(word, spoken_word):
        return min(score, 20)

    return max(score, 50)

def practice_session(user_id):
    """
    Runs an interactive pronunciation practice session for a logged-in user.
    """
    console.clear()
    console.print("[bold cyan]Pronunciation Practice[/bold cyan]\n")

    difficulty_choice = Prompt.ask(
        "Choose difficulty\n[1] Beginner\n[2] Intermediate\n[3] Advanced",
        choices=["1", "2", "3"],
        default="1",
        show_choices=False,
        show_default=False
    )
    difficulty = DIFFICULTY_MAP[difficulty_choice]

    while True:
        word = get_random_word(difficulty=difficulty)
        if word is None:
            console.print("[red]No words found for this difficulty.[/red]")
            input("Press Enter to continue...")
            return

        repeat_word = True
        while repeat_word:
            console.print(f"[bold yellow]Word:[/bold yellow] {word}\n")

            hear_it = Prompt.ask(
                "Let's hear pronunciation?(y/n)",
                choices=["y", "n"], default="y",
                show_choices=False, show_default=False
            )
            if hear_it == "y":
                speak(word)

            ref_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            user_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name

            generate_reference(word, ref_path)
            captured = record_audio(user_path)

            if not captured:
                console.print("\n[red]No speech detected.[/red]\n")
                os.remove(ref_path)
                os.remove(user_path)

                retry = Prompt.ask(
                    "Try again?", choices=["y", "n"], default="y",
                    show_choices=False, show_default=False
                )
                if retry == "y":
                    continue
                return

            score = score_attempt(word, ref_path, user_path)
            os.remove(ref_path)
            os.remove(user_path)

            console.print()
            console.print(f"[cyan]Word     :[/cyan] {word}")
            console.print(f"[cyan]Score    :[/cyan] {format_score(score)}")
            console.print(f"[cyan]Feedback :[/cyan] {get_performance(score)}")

            save_attempt(user_id=user_id, word=word, score=score, attempts=1)

            console.print()
            again_same = Prompt.ask(
                "Practice this word again?(y/n)",
                choices=["y", "n"], default="n",
                show_choices=False, show_default=False
            )
            repeat_word = again_same == "y"

        again = Prompt.ask(
            "Practice another word?(y/n)",
            choices=["y", "n"], default="y",
            show_choices=False, show_default=False
        )
        if again == "n":
            break