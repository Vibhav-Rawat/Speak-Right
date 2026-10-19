from unittest.mock import patch
from project import display_title, get_main_menu_choice, get_dashboard_choice
from utils import (
    calculate_similarity,
    format_score,
    get_performance,
    validate_username,
    validate_password,
    normalize_text,
    word_matches,
)

def test_display_title():
    """Test that the application title is displayed."""
    with patch("project.console.print") as mock_print:
        display_title()
        mock_print.assert_called_once()


def test_get_main_menu_choice():
    """Test the main menu input."""
    with patch("project.Prompt.ask", return_value="2") as mock_prompt:
        assert get_main_menu_choice() == "2"
        mock_prompt.assert_called_once()


def test_get_dashboard_choice():
    """Test the dashboard menu input."""
    with patch("project.Prompt.ask", return_value="4") as mock_prompt:
        assert get_dashboard_choice() == "4"
        mock_prompt.assert_called_once()

def test_calculate_similarity():
    """Test text similarity calculations."""
    assert calculate_similarity("hello", "hello") == 100.0
    assert calculate_similarity("Hello", "hello") == 100.0
    assert calculate_similarity("hello", "world") < 50.0
    assert calculate_similarity("", "") == 100.0


def test_format_score():
    """Test formatting of percentage scores."""
    assert format_score(85) == "85.00%"
    assert format_score(0) == "0.00%"
    assert format_score(100) == "100.00%"
    assert format_score(72.456) == "72.46%"


def test_get_performance():
    """Test feedback for different score ranges."""
    assert get_performance(97) == "Excellent!"
    assert get_performance(90) == "Great Job!"
    assert get_performance(75) == "Good"
    assert get_performance(55) == "Keep Practicing"
    assert get_performance(20) == "Needs Improvement"


    assert get_performance(95) == "Excellent!"
    assert get_performance(85) == "Great Job!"
    assert get_performance(70) == "Good"
    assert get_performance(50) == "Keep Practicing"
    assert get_performance(49) == "Needs Improvement"


def test_validate_username():
    """Test username validation."""
    assert validate_username("Vibhav") is True
    assert validate_username("valid123") is True
    assert validate_username("ab") is False
    assert validate_username("this_username_is_way_too_long") is False
    assert validate_username("user name") is False
    assert validate_username("user123!") is False
    assert validate_username("   ") is False
    assert validate_username(" abc ") is True


def test_validate_password():
    """Test password length validation."""
    assert validate_password("abcdef") is True
    assert validate_password("123456") is True
    assert validate_password("abcde") is False
    assert validate_password("") is False


def test_normalize_text():
    """Test lowercase conversion and whitespace removal."""
    assert normalize_text("  Hello  ") == "hello"
    assert normalize_text("KING") == "king"
    assert normalize_text(" jet ") == "jet"


def test_word_matches():
    """Test matching of target and recognized words."""
    assert word_matches("king", "king") is True
    assert word_matches("KING", "king") is True
    assert word_matches(" jet ", "jet") is True
    assert word_matches("king", None) is False
    assert word_matches("king", "completely different") is False