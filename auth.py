import hashlib
from rich.console import Console
from rich.prompt import Prompt
from database import get_user, add_user
import pwinput

console = Console()


def hash_password(password):
    """
    Returns the SHA-256 hash of a password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def username_exists(username):
    """
    Returns True if the username already exists.
    """
    return get_user(username) is not None


def register():
    """
    Prompts for a new username/password and creates the account.
    """
    console.print("\n[bold cyan]Create Account[/bold cyan]\n")

    while True:
        username = Prompt.ask("Username").strip()
        if not username:
            console.print("[red]Username cannot be empty.[/red]")
        elif username_exists(username):
            console.print("[red]Username already exists.[/red]")
        else:
            break

    while True:
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        confirm = pwinput.pwinput(prompt="Confirm Password: ", mask="*")
        if password != confirm:
            console.print("[red]Passwords do not match.[/red]")
        elif len(password) < 6:
            console.print("[red]Password must contain at least 6 characters.[/red]")
        else:
            break

    add_user(username, hash_password(password))

    console.print("\n[green]Account created successfully![/green]")
    input("\nPress Enter to continue...")


def login():
    """
    Authenticates an existing user. Returns their user ID, or None on failure.
    """
    console.print("\n[bold cyan]Login[/bold cyan]\n")

    username = Prompt.ask("Username")
    password = pwinput.pwinput(prompt="Password: ", mask="*")

    user = get_user(username)

    if user is None:
        console.print("[red]User not found.[/red]")
        input("\nPress Enter to continue...")
        return None

    user_id, _, stored_password = user

    if hash_password(password) != stored_password:
        console.print("[red]Incorrect password.[/red]")
        input("\nPress Enter to continue...")
        return None

    console.print(f"\n[green]Welcome, {username}![/green]")
    input("\nPress Enter to continue...")
    return user_id