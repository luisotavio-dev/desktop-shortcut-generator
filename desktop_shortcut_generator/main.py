"""Desktop Shortcut Generator - Entry point."""

import sys

from PyQt6.QtWidgets import QApplication

from desktop_shortcut_generator.config.settings import APP_NAME
from desktop_shortcut_generator.i18n import detect_system_language, set_language
from desktop_shortcut_generator.infrastructure.file_writer import DesktopFileWriter
from desktop_shortcut_generator.presentation.main_window import MainWindow
from desktop_shortcut_generator.use_cases.create_shortcut import CreateShortcutUseCase


def main() -> int:
    """Initialize dependencies and launch the application.

    Returns:
        The application exit code.
    """
    set_language(detect_system_language())

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    writer = DesktopFileWriter()
    use_case = CreateShortcutUseCase(writer)
    window = MainWindow(use_case)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
