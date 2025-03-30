"""Main entry point for the voice typing application."""


def main() -> None:
    """Run the voice typing application."""
    # Application startup logic will go here


def process_commands(commands: list[str]) -> list[str]:
    """Process voice commands.

    Args:
        commands: List of voice commands to process

    Returns:
        List of processed commands
    """
    return [cmd.lower() for cmd in commands]


if __name__ == "__main__":
    main()
