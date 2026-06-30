"""XDG Base Directory path resolution for Linux desktop environments."""

import os
import re
from pathlib import Path

_FALLBACK_DESKTOP_DIR_NAMES: tuple[str, ...] = (
    "Desktop",
    "Área de Trabalho",
    "Escritorio",
    "Schreibtisch",
    "Bureau",
)

_USER_DIRS_CONFIG: Path = Path.home() / ".config" / "user-dirs.dirs"
_USER_DIRS_PATTERN: re.Pattern[str] = re.compile(
    r'^XDG_DESKTOP_DIR="(?P<path>(?:\$HOME)?[^"]+)"\s*$'
)


def resolve_applications_dir() -> Path:
    """Resolve the user applications directory following XDG conventions.

    Returns:
        Path to ``$XDG_DATA_HOME/applications`` or the default location.
    """
    data_home = os.environ.get("XDG_DATA_HOME", "").strip()
    if data_home:
        return Path(data_home).expanduser() / "applications"
    return Path.home() / ".local" / "share" / "applications"


def _parse_user_dirs_desktop() -> Path | None:
    """Read the desktop directory from ``user-dirs.dirs`` if configured."""
    if not _USER_DIRS_CONFIG.is_file():
        return None

    try:
        content = _USER_DIRS_CONFIG.read_text(encoding="utf-8")
    except OSError:
        return None

    home = str(Path.home())
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = _USER_DIRS_PATTERN.match(line)
        if not match:
            continue

        raw_path = match.group("path").replace("$HOME", home)
        return Path(raw_path).expanduser()

    return None


def resolve_desktop_dir() -> Path | None:
    """Resolve the user desktop directory across desktop environments.

    Resolution order:
        1. ``XDG_DESKTOP_DIR`` from ``~/.config/user-dirs.dirs``
        2. Common localized folder names under the home directory
        3. ``None`` when no desktop directory can be determined

    Returns:
        The desktop directory path, or ``None`` if unavailable.
    """
    configured_desktop = _parse_user_dirs_desktop()
    if configured_desktop is not None:
        return configured_desktop

    home = Path.home()
    for dir_name in _FALLBACK_DESKTOP_DIR_NAMES:
        desktop_path = home / dir_name
        if desktop_path.is_dir():
            return desktop_path

    return None


def resolve_output_dir() -> tuple[Path, bool]:
    """Choose where to save a new shortcut file.

    Returns:
        A tuple of ``(output_directory, is_desktop)``. Falls back to the
        applications directory when no desktop folder is available.
    """
    desktop_dir = resolve_desktop_dir()
    if desktop_dir is not None:
        return desktop_dir, True
    return resolve_applications_dir(), False
