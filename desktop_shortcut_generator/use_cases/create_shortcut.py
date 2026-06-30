"""Use case for creating desktop shortcuts."""

from pathlib import Path
from typing import Protocol

from desktop_shortcut_generator.domain.entities import Shortcut


class DesktopWriterProtocol(Protocol):
    """Protocol for desktop file writers."""

    def write(self, content: str, app_name: str) -> Path:
        """Write shortcut content to disk."""
        ...


class CreateShortcutUseCase:
    """Orchestrates validation and persistence of desktop shortcuts."""

    def __init__(self, writer: DesktopWriterProtocol) -> None:
        """Initialize the use case with a file writer dependency.

        Args:
            writer: Component responsible for writing .desktop files.
        """
        self._writer = writer

    def execute(self, shortcut: Shortcut) -> Path:
        """Validate and persist a desktop shortcut.

        Args:
            shortcut: The shortcut entity to create.

        Returns:
            The path where the .desktop file was saved.
        """
        shortcut.validate()
        content = shortcut.to_desktop_content()
        return self._writer.write(content, shortcut.name)
