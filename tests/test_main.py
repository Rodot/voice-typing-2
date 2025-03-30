"""Tests for the main module."""

from voice_typing.main import process_commands


def test_process_commands() -> None:
    """Test the process_commands function."""
    # Given
    commands = ["Hello", "WORLD", "Test"]

    # When
    result = process_commands(commands)

    # Then
    assert result == ["hello", "world", "test"]


def test_process_commands_empty() -> None:
    """Test the process_commands function with empty input."""
    # Given
    commands: list[str] = []

    # When
    result = process_commands(commands)

    # Then
    assert result == []
