"""Compile .po translation files to .mo binaries."""

import subprocess
import sys
from pathlib import Path

LOCALES_DIR = (
    Path(__file__).resolve().parent.parent
    / "desktop_shortcut_generator"
    / "i18n"
    / "locales"
)


def compile_translations() -> int:
    """Compile all .po files under locales/ to .mo files.

    Returns:
        Exit code (0 on success, 1 on failure).
    """
    po_files = list(LOCALES_DIR.glob("*/LC_MESSAGES/messages.po"))
    if not po_files:
        print("No .po files found.")
        return 1

    errors = 0
    for po_file in po_files:
        mo_file = po_file.with_suffix(".mo")
        result = subprocess.run(
            ["msgfmt", "-o", str(mo_file), str(po_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"Failed to compile {po_file}: {result.stderr}")
            errors += 1
        else:
            print(f"Compiled {mo_file}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(compile_translations())
