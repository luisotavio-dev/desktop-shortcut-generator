"""Main application window for Desktop Shortcut Generator."""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPalette, QShowEvent
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from desktop_shortcut_generator.config.settings import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_ICON,
    SUPPORTED_LANGUAGES,
)
from desktop_shortcut_generator.domain.entities import Shortcut
from desktop_shortcut_generator.domain.exceptions import (
    DomainError,
    FileWriteError,
    ValidationError,
)
from desktop_shortcut_generator.i18n import _, get_current_language, set_language
from desktop_shortcut_generator.presentation.components import FileSelector, IconSelector
from desktop_shortcut_generator.use_cases.create_shortcut import CreateShortcutUseCase

_VALIDATION_MESSAGES: dict[str, str] = {
    "Application name is required": "Application name is required",
    "Executable path does not exist": "Executable path does not exist",
    "Executable path must be a file": "Executable path must be a file",
    "Icon path does not exist": "Icon path does not exist",
    "Icon path must be a file": "Icon path must be a file",
}


class MainWindow(QMainWindow):
    """Primary window for creating desktop shortcuts."""

    def __init__(self, create_shortcut_use_case: CreateShortcutUseCase) -> None:
        """Initialize the main window.

        Args:
            create_shortcut_use_case: Use case injected from the composition root.
        """
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint
        )
        self._create_shortcut_use_case = create_shortcut_use_case
        self._build_ui()
        self._connect_signals()
        self.retranslate_ui()

        icon_path = Path(DEFAULT_ICON)
        if icon_path.is_file():
            self.setWindowIcon(QIcon(str(icon_path)))

    def showEvent(self, event: QShowEvent) -> None:
        """Set initial focus to the application name field when the window opens."""
        super().showEvent(event)
        self._name_edit.setFocus()

    def _build_ui(self) -> None:
        """Construct all widgets and layouts."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self._title_label = QLabel()
        self._subtitle_label = QLabel()

        self._shortcut_group = QGroupBox()
        self._options_group = QGroupBox()

        self._name_edit = QLineEdit()
        self._name_edit.setClearButtonEnabled(True)
        self._exec_selector = FileSelector(
            _("Select Executable"),
            f"{_('Executables')} (*.sh *.py *.bin);;{_('All Files')} (*)",
        )
        self._icon_selector = IconSelector(
            _("Select Shortcut Icon"),
            f"{_('Images')} (*.png *.svg *.xpm *.jpg *.jpeg);;{_('All Files')} (*)",
        )
        self._comment_edit = QLineEdit()
        self._comment_edit.setClearButtonEnabled(True)
        self._terminal_checkbox = QCheckBox()
        self._language_combo = QComboBox()
        self._language_combo.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        self._language_combo.setMinimumWidth(160)
        self._create_button = QPushButton()
        self._create_button.setDefault(True)
        self._create_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        self._create_button.setMinimumWidth(180)
        self._version_label = QLabel()

        for code, label in SUPPORTED_LANGUAGES.items():
            self._language_combo.addItem(label, code)

        current_lang = get_current_language()
        index = self._language_combo.findData(current_lang)
        if index >= 0:
            self._language_combo.setCurrentIndex(index)

        shortcut_form = QFormLayout()
        shortcut_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        shortcut_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        shortcut_form.setFormAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        shortcut_form.setHorizontalSpacing(16)
        shortcut_form.setVerticalSpacing(12)

        self._name_label = QLabel()
        self._exec_label = QLabel()
        self._icon_label = QLabel()
        self._comment_label = QLabel()

        shortcut_form.addRow(self._name_label, self._name_edit)
        shortcut_form.addRow(self._exec_label, self._exec_selector)
        shortcut_form.addRow(self._icon_label, self._icon_selector)
        shortcut_form.addRow(self._comment_label, self._comment_edit)
        self._shortcut_group.setLayout(shortcut_form)

        options_form = QFormLayout()
        options_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        options_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        options_form.setHorizontalSpacing(16)
        options_form.setVerticalSpacing(10)

        self._terminal_label = QLabel()
        options_form.addRow(self._terminal_label, self._terminal_checkbox)
        self._options_group.setLayout(options_form)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()
        header_layout.addWidget(
            self._language_combo,
            alignment=Qt.AlignmentFlag.AlignVCenter,
        )

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self._create_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 16)
        main_layout.setSpacing(14)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self._subtitle_label)
        main_layout.addWidget(self._shortcut_group)
        main_layout.addWidget(self._options_group)
        main_layout.addWidget(separator)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(
            self._version_label,
            alignment=Qt.AlignmentFlag.AlignRight,
        )
        central_widget.setLayout(main_layout)

        self._apply_header_style()
        self.setMinimumWidth(600)

    def _apply_header_style(self) -> None:
        """Style the window header using standard fonts and palette roles."""
        title_font = QFont(self._title_label.font())
        title_font.setPointSize(title_font.pointSize() + 3)
        title_font.setWeight(QFont.Weight.DemiBold)
        self._title_label.setFont(title_font)

        subtitle_font = QFont(self._subtitle_label.font())
        if subtitle_font.pointSize() > 0:
            subtitle_font.setPointSize(max(subtitle_font.pointSize() - 1, 8))
        self._subtitle_label.setFont(subtitle_font)

        subtitle_palette = self._subtitle_label.palette()
        subtitle_palette.setColor(
            QPalette.ColorRole.WindowText,
            subtitle_palette.color(QPalette.ColorRole.PlaceholderText),
        )
        self._subtitle_label.setPalette(subtitle_palette)
        self._subtitle_label.setWordWrap(True)

        version_font = QFont(self._version_label.font())
        if version_font.pointSize() > 0:
            version_font.setPointSize(max(version_font.pointSize() - 1, 8))
        self._version_label.setFont(version_font)

        version_palette = self._version_label.palette()
        version_palette.setColor(
            QPalette.ColorRole.WindowText,
            version_palette.color(QPalette.ColorRole.PlaceholderText),
        )
        self._version_label.setPalette(version_palette)

    def _connect_signals(self) -> None:
        """Wire UI signals to handlers."""
        self._create_button.clicked.connect(self._on_create_shortcut)
        self._language_combo.currentIndexChanged.connect(self._on_language_changed)

    def retranslate_ui(self) -> None:
        """Refresh all translatable strings in the UI."""
        self.setWindowTitle(APP_NAME)
        self._title_label.setText(APP_NAME)
        self._subtitle_label.setText(
            _("Create a .desktop shortcut for your application.")
        )
        self._shortcut_group.setTitle(_("Shortcut Details"))
        self._options_group.setTitle(_("Options"))
        self._name_label.setText(_("Application Name"))
        self._exec_label.setText(_("Executable Path"))
        self._icon_label.setText(_("Shortcut Icon Path"))
        self._comment_label.setText(_("Description"))
        self._terminal_label.setText(_("Run in Terminal"))
        self._language_combo.setToolTip(_("Language"))
        self._language_combo.setAccessibleName(_("Language"))
        self._create_button.setText(_("Create Shortcut"))
        self._version_label.setText(_("Version {version}").format(version=APP_VERSION))

        self._name_edit.setPlaceholderText(_("e.g. My Application"))
        self._comment_edit.setPlaceholderText(_("Optional description shown in menus"))

        self._exec_selector.set_dialog_title(_("Select Executable"))
        self._icon_selector.set_dialog_title(_("Select Shortcut Icon"))
        self._exec_selector.retranslate()
        self._icon_selector.retranslate()
        self._apply_fixed_size()

    def _apply_fixed_size(self) -> None:
        """Lock the window to its natural size and prevent resizing."""
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        self.setMinimumWidth(600)
        self.adjustSize()
        self.setFixedSize(self.size())

    def _on_language_changed(self) -> None:
        """Handle language selection changes."""
        lang_code = self._language_combo.currentData()
        if lang_code:
            set_language(lang_code)
            self.retranslate_ui()

    def _translate_validation_message(self, message: str) -> str:
        """Translate a domain validation message key."""
        key = _VALIDATION_MESSAGES.get(message, message)
        return _(key)

    def _on_create_shortcut(self) -> None:
        """Handle the create shortcut button click."""
        shortcut = Shortcut(
            name=self._name_edit.text(),
            exec_path=self._exec_selector.text(),
            icon_path=self._icon_selector.text(),
            comment=self._comment_edit.text(),
            terminal=self._terminal_checkbox.isChecked(),
        )

        try:
            file_path = self._create_shortcut_use_case.execute(shortcut)
        except ValidationError as exc:
            QMessageBox.warning(
                self,
                _("Validation Error"),
                self._translate_validation_message(exc.message),
            )
            return
        except FileWriteError as exc:
            QMessageBox.critical(self, _("File Error"), str(exc))
            return
        except DomainError as exc:
            QMessageBox.critical(self, _("Error"), str(exc))
            return

        QMessageBox.information(
            self,
            _("Success"),
            _("Shortcut created successfully at:\n{path}").format(path=file_path),
        )
