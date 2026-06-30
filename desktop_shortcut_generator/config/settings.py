"""Global application settings for Desktop Shortcut Generator."""

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
APP_NAME: str = "Desktop Shortcut Generator"
APP_VERSION: str = "1.0.0"
DEFAULT_ICON: str = str(BASE_DIR / "assets" / "app-icon.png")

LOCALES_DIR: Path = BASE_DIR / "i18n" / "locales"
SUPPORTED_LANGUAGES: dict[str, str] = {
    "pt_BR": "Português (Brasil)",
    "en": "English",
    "es": "Español",
}

SUPPORTED_ICON_EXTENSIONS: tuple[str, ...] = (".png", ".svg", ".xpm", ".jpg", ".jpeg")
SUPPORTED_ICON_FORMATS: str = "PNG, SVG, XPM, JPG, JPEG"
