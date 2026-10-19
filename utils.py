import librosa
from librosa.sequence import dtw
from rapidfuzz import fuzz


def get_mfcc(filepath):
    """
    Loads an audio file and returns its MFCC feature matrix.
    """
    y, sr = librosa.load(filepath, sr=16000)
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)


def compare_audio(reference_path, user_path):
    """
    Compares user audio to reference audio using MFCC + DTW.
    Returns a similarity score from 0-100.
    """

    ref_mfcc = get_mfcc(reference_path)
    user_mfcc = get_mfcc(user_path)

    D, wp = dtw(ref_mfcc, user_mfcc)
    distance = D[-1, -1] / len(wp)

    SCALE = 550  

    score = max(0, 100 - (distance / SCALE * 100))
    distance = D[-1, -1] / len(wp)
    print(f"Audio Difference Score: {distance}")

    return round(score, 2)


def calculate_similarity(expected, spoken):
    """
    Returns the similarity score (0-100)
    between the expected and spoken text.
    (Kept for optional text-based fallback / testing.)
    """

    expected = expected.strip().lower()
    spoken = spoken.strip().lower()

    return round(fuzz.ratio(expected, spoken), 2)


def validate_username(username):
    """
    Returns True if the username is valid.
    """

    username = username.strip()

    if len(username) < 3:
        return False

    if len(username) > 20:
        return False

    return username.isalnum()


def validate_password(password):
    """
    Returns True if password meets requirements.
    """

    return len(password) >= 6


def format_score(score):
    """
    Returns a formatted percentage string.
    """

    return f"{score:.2f}%"


def get_performance(score):
    """
    Returns a performance message based on score.
    """

    if score >= 95:
        return "Excellent!"

    elif score >= 85:
        return "Great Job!"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Keep Practicing"

    return "Needs Improvement"


def normalize_text(text):
    """
    Removes leading/trailing spaces
    and converts text to lowercase.
    """

    return text.strip().lower()

def word_matches(expected, recognized, threshold=70):
    """
    Returns True if the recognized word is similar enough to the expected word.
    """
    if recognized is None:
        return False

    expected = expected.strip().lower()
    recognized = recognized.strip().lower()

    return fuzz.ratio(expected, recognized) >= threshold