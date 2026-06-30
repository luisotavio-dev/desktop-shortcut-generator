"""Mark desktop shortcuts as trusted for GNOME and similar environments."""

import shutil
import subprocess
from pathlib import Path


def mark_desktop_file_trusted(file_path: Path) -> None:
    """Mark a ``.desktop`` file as trusted so it can be launched from the desktop.

    GNOME and some other environments require the ``metadata::trusted`` attribute
    in addition to executable permissions. Uses ``gio`` when available.

    Args:
        file_path: Path to the ``.desktop`` file on the user's desktop.
    """
    if not file_path.is_file() or shutil.which("gio") is None:
        return

    subprocess.run(
        ["gio", "set", str(file_path), "metadata::trusted", "true"],
        check=False,
        capture_output=True,
    )
