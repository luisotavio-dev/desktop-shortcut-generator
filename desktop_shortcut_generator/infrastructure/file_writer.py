"""File system operations for writing .desktop shortcut files."""

import stat
from pathlib import Path

from desktop_shortcut_generator.domain.exceptions import FileWriteError
from desktop_shortcut_generator.infrastructure.desktop_trust import (
    mark_desktop_file_trusted,
)
from desktop_shortcut_generator.infrastructure.xdg_paths import resolve_output_dir


class DesktopFileWriter:
    """Writes .desktop files to the user's desktop or applications directory."""

    def _sanitize_filename(self, name: str) -> str:
        """Create a safe filename from the application name.

        Args:
            name: The application display name.

        Returns:
            A sanitized filename ending with .desktop.
        """
        safe_chars = []
        for char in name.strip():
            if char.isalnum() or char in (" ", "-", "_"):
                safe_chars.append(char)
            else:
                safe_chars.append("_")
        safe_name = "".join(safe_chars).strip().replace(" ", "-")
        if not safe_name:
            safe_name = "shortcut"
        return f"{safe_name}.desktop"

    def write(self, content: str, app_name: str) -> Path:
        """Write a .desktop file and set executable permissions.

        When saving to the desktop, also attempts to mark the file as trusted
        for GNOME-based environments.

        Args:
            content: The .desktop file content.
            app_name: The application name used for the filename.

        Returns:
            The path to the written .desktop file.

        Raises:
            FileWriteError: If the file cannot be written or chmod fails.
        """
        output_dir, is_desktop = resolve_output_dir()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise FileWriteError(
                f"Cannot create output directory '{output_dir}': {exc}"
            ) from exc

        file_path = output_dir / self._sanitize_filename(app_name)
        try:
            file_path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise FileWriteError(
                f"Cannot write shortcut file '{file_path}': {exc}"
            ) from exc

        try:
            current_mode = file_path.stat().st_mode
            file_path.chmod(
                current_mode
                | stat.S_IXUSR
                | stat.S_IXGRP
                | stat.S_IXOTH
            )
        except OSError as exc:
            raise FileWriteError(
                f"Cannot set execute permissions on '{file_path}': {exc}"
            ) from exc

        if is_desktop:
            mark_desktop_file_trusted(file_path)

        return file_path
