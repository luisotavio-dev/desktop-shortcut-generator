"""Reusable UI components for Desktop Shortcut Generator."""

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from desktop_shortcut_generator.config.settings import SUPPORTED_ICON_FORMATS
from desktop_shortcut_generator.i18n import _


class FileSelector(QWidget):
    """A line edit with a browse button for selecting files."""

    path_changed = pyqtSignal(str)

    def __init__(
        self,
        dialog_title: str,
        file_filter: str = "",
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the file selector widget.

        Args:
            dialog_title: Title shown in the file dialog.
            file_filter: Qt file filter string for the dialog.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._dialog_title = dialog_title
        self._file_filter = file_filter

        self._path_edit = QLineEdit()
        self._path_edit.setClearButtonEnabled(True)
        self._path_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self._browse_button = QPushButton(_("Browse..."))
        self._browse_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(self._path_edit)
        layout.addWidget(self._browse_button)
        self.setLayout(layout)

        self._browse_button.clicked.connect(self._open_file_dialog)
        self._path_edit.textChanged.connect(self.path_changed.emit)

    def _open_file_dialog(self) -> None:
        """Open a file dialog and set the selected path."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self._dialog_title,
            "",
            self._file_filter,
        )
        if file_path:
            self._path_edit.setText(file_path)

    def text(self) -> str:
        """Return the current file path text."""
        return self._path_edit.text().strip()

    def set_text(self, value: str) -> None:
        """Set the file path text."""
        self._path_edit.setText(value)

    def set_dialog_title(self, title: str) -> None:
        """Update the file dialog title (used when language changes)."""
        self._dialog_title = title

    def set_file_filter(self, file_filter: str) -> None:
        """Update the file dialog filter (used when language changes)."""
        self._file_filter = file_filter

    def retranslate(self) -> None:
        """Refresh translatable UI strings."""
        self._browse_button.setText(_("Browse..."))


class IconSelector(QWidget):
    """File selector for shortcut icon images with a live preview."""

    _PREVIEW_SIZE: int = 72

    def __init__(
        self,
        dialog_title: str,
        file_filter: str = "",
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the icon selector with preview.

        Args:
            dialog_title: Title shown in the file dialog.
            file_filter: Qt file filter string for the dialog.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._dialog_title = dialog_title
        self._file_filter = file_filter

        self._preview_frame = QFrame()
        self._preview_frame.setFixedSize(self._PREVIEW_SIZE, self._PREVIEW_SIZE)
        self._preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._preview_frame.setFrameShadow(QFrame.Shadow.Sunken)

        self._preview_label = QLabel(self._preview_frame)
        self._preview_label.setGeometry(0, 0, self._PREVIEW_SIZE, self._PREVIEW_SIZE)
        self._preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._selector = FileSelector(dialog_title, file_filter)
        self._hint_label = QLabel()
        self._hint_label.setWordWrap(True)
        self._apply_hint_style()

        selector_layout = QVBoxLayout()
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(6)
        selector_layout.addWidget(self._selector)
        selector_layout.addWidget(self._hint_label)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self._preview_frame, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(selector_layout)
        self.setLayout(layout)

        self._selector.path_changed.connect(self._update_preview)
        self.retranslate()

    def _apply_hint_style(self) -> None:
        """Use palette colors for secondary hint text."""
        hint_font = QFont(self._hint_label.font())
        if hint_font.pointSize() > 0:
            hint_font.setPointSize(max(hint_font.pointSize() - 1, 8))
        self._hint_label.setFont(hint_font)

        palette = self._hint_label.palette()
        palette.setColor(
            QPalette.ColorRole.WindowText,
            palette.color(QPalette.ColorRole.PlaceholderText),
        )
        self._hint_label.setPalette(palette)

    def _update_preview(self, path: str) -> None:
        """Refresh the icon preview from the given image path."""
        image_path = Path(path.strip()).expanduser()
        if image_path.is_file():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self._PREVIEW_SIZE - 12,
                    self._PREVIEW_SIZE - 12,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self._preview_label.setText("")
                self._preview_label.setPixmap(scaled)
                return

        self._preview_label.setPixmap(QPixmap())
        self._preview_label.setText(_("No preview"))

    def text(self) -> str:
        """Return the current shortcut icon path."""
        return self._selector.text()

    def set_dialog_title(self, title: str) -> None:
        """Update the file dialog title (used when language changes)."""
        self._dialog_title = title
        self._selector.set_dialog_title(title)

    def retranslate(self) -> None:
        """Refresh translatable UI strings."""
        self._hint_label.setText(
            _("Image file used as the shortcut icon. "
              "Supported formats: {formats}.").format(formats=SUPPORTED_ICON_FORMATS)
        )
        self._selector.retranslate()
        self._update_preview(self._selector.text())
