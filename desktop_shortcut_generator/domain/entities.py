"""Domain entities for Desktop Shortcut Generator."""

from dataclasses import dataclass
from pathlib import Path

from desktop_shortcut_generator.domain.exceptions import ValidationError


def _quote_desktop_value(value: str) -> str:
    """Quote a .desktop field value when it contains reserved characters."""
    if any(char in value for char in ('"', "\\", "$", "`")):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if " " in value:
        return f'"{value}"'
    return value


@dataclass
class Shortcut:
    """Represents a Linux desktop shortcut (.desktop file).

    Attributes:
        name: Display name of the application.
        exec_path: Absolute path to the executable file.
        icon_path: Absolute path to the icon image file.
        comment: Short description shown by desktop environments.
        terminal: Whether the application should run inside a terminal.
    """

    name: str
    exec_path: str
    icon_path: str
    comment: str
    terminal: bool = False

    def validate(self) -> None:
        """Validate all shortcut fields before persistence.

        Raises:
            ValidationError: If any field contains invalid data.
        """
        if not self.name.strip():
            raise ValidationError("name", "Application name is required")

        exec_path = Path(self.exec_path).expanduser().resolve()
        if not exec_path.exists():
            raise ValidationError("exec_path", "Executable path does not exist")
        if not exec_path.is_file():
            raise ValidationError("exec_path", "Executable path must be a file")

        icon_path = Path(self.icon_path).expanduser().resolve()
        if not icon_path.exists():
            raise ValidationError("icon_path", "Icon path does not exist")
        if not icon_path.is_file():
            raise ValidationError("icon_path", "Icon path must be a file")

    def to_desktop_content(self) -> str:
        """Build a FreeDesktop.org compliant .desktop file content.

        Returns:
            The serialized .desktop file content.
        """
        exec_path = str(Path(self.exec_path).expanduser().resolve())
        icon_path = str(Path(self.icon_path).expanduser().resolve())
        terminal_value = "true" if self.terminal else "false"

        lines = [
            "[Desktop Entry]",
            "Version=1.5",
            "Type=Application",
            f"Name={self.name.strip()}",
            f"Comment={self.comment.strip()}",
            f"Exec={_quote_desktop_value(exec_path)}",
            f"Icon={_quote_desktop_value(icon_path)}",
            f"Terminal={terminal_value}",
            "Categories=Utility;",
        ]
        return "\n".join(lines) + "\n"
