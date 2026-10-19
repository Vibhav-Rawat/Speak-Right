import sqlite3
import random
from pathlib import Path
from contextlib import contextmanager

DATABASE_NAME = "pronunciation.db"


@contextmanager
def db_cursor(commit=False):
    """
    Yields a cursor for a single database operation and closes the
    connection afterward. Commits first if commit=True.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn.cursor()
        if commit:
            conn.commit()
    finally:
        conn.close()


def initialize_database():
    """
    Creates all required tables and loads words if the words table is empty.
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS words(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                difficulty TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                score REAL NOT NULL,
                attempts INTEGER NOT NULL,
                practice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
    load_words()


def add_user(username, password):
    """
    Adds a new user with an already-hashed password.
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, password)
        )


def get_user(username):
    """
    Returns (id, username, password) for a user, or None if not found.
    """
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        return cursor.fetchone()


def add_word(word, difficulty):
    """
    Adds a single word under the given difficulty, ignoring duplicates.
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT OR IGNORE INTO words(word, difficulty) VALUES(?, ?)",
            (word.lower(), difficulty)
        )


def get_random_word(difficulty=None):
    """
    Returns a random word, optionally filtered by difficulty.
    Returns None if no words are available.
    """
    with db_cursor() as cursor:
        if difficulty:
            cursor.execute("SELECT word FROM words WHERE difficulty = ?", (difficulty,))
        else:
            cursor.execute("SELECT word FROM words")
        words = cursor.fetchall()

    return random.choice(words)[0] if words else None


def save_attempt(user_id, word, score, attempts):
    """
    Records one pronunciation attempt in the history table.
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO history(user_id, word, score, attempts)
            VALUES(?, ?, ?, ?)
            """,
            (user_id, word, score, attempts)
        )


def get_history(user_id):
    """
    Returns every practice attempt for a user, most recent first.
    """
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT word, score, attempts, practice_date
            FROM history
            WHERE user_id = ?
            ORDER BY practice_date DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()


def get_statistics(user_id):
    """
    Returns (total_attempts, average_score, highest_score, lowest_score).
    """
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*), AVG(score), MAX(score), MIN(score)
            FROM history
            WHERE user_id = ?
            """,
            (user_id,)
        )
        return cursor.fetchone()


def get_weak_words(user_id):
    """
    Returns (word, average_score) pairs for words averaging below 70.
    """
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT word, AVG(score)
            FROM history
            WHERE user_id = ?
            GROUP BY word
            HAVING AVG(score) < 70
            ORDER BY AVG(score)
            """,
            (user_id,)
        )
        return cursor.fetchall()


def load_words():
    """
    Loads words from the words/ folder into the database.
    Skips entirely if the words table already has data.
    """
    with db_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM words")
        if cursor.fetchone()[0] > 0:
            return

    words_folder = Path(__file__).parent / "words"
    files = {
        "beginner.txt": "Beginner",
        "intermediate.txt": "Intermediate",
        "advanced.txt": "Advanced"
    }

    with db_cursor(commit=True) as cursor:
        for filename, difficulty in files.items():
            file_path = words_folder / filename
            if not file_path.exists():
                continue

            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip()
                    if word:
                        cursor.execute(
                            "INSERT OR IGNORE INTO words(word, difficulty) VALUES(?, ?)",
                            (word.lower(), difficulty)
                        )