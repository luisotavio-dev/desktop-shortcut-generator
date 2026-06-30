"""Gettext-based translation utilities."""

import gettext
import locale
import os
from typing import Optional

from desktop_shortcut_generator.config.settings import LOCALES_DIR, SUPPORTED_LANGUAGES

_current_translator: Optional[gettext.NullTranslations] = None
_current_language: str = "en"

_FALLBACK_LANGUAGE: str = "en"
_LOCALE_ENV_VARS: tuple[str, ...] = ("LC_ALL", "LC_MESSAGES", "LANG")


def _normalize_locale_tag(tag: str) -> str:
    """Normalize a locale tag to a lowercase language identifier.

    Examples:
        pt_BR.UTF-8 -> pt_br
        en-US -> en_us
    """
    return tag.strip().replace("-", "_").split(".")[0].lower()


def _match_supported_language(tag: str) -> Optional[str]:
    """Map a locale tag to a supported language code, if possible."""
    normalized = _normalize_locale_tag(tag)
    if not normalized or normalized == "c":
        return None

    if normalized.startswith("pt"):
        return "pt_BR"
    if normalized.startswith("es"):
        return "es"
    if normalized.startswith("en"):
        return "en"
    return None


def _locale_candidates() -> list[str]:
    """Collect locale candidates from environment and libc settings."""
    candidates: list[str] = []

    for var in _LOCALE_ENV_VARS:
        value = os.environ.get(var, "").strip()
        if value:
            candidates.append(value)

    try:
        language_code, _ = locale.getlocale(locale.LC_MESSAGES)
        if language_code:
            candidates.append(language_code)
    except (locale.Error, ValueError, TypeError):
        pass

    try:
        default_locale, _ = locale.getdefaultlocale()
        if default_locale:
            candidates.append(default_locale)
    except (locale.Error, ValueError, TypeError):
        pass

    return candidates


def detect_system_language() -> str:
    """Detect the best supported language from the operating system.

    Reads Linux locale settings (``LANG``, ``LC_MESSAGES``, ``LC_ALL``) and
    libc locale information. Returns English when the system language is not
    supported or cannot be determined.

    Returns:
        A supported language code (``pt_BR``, ``en``, or ``es``).
    """
    for candidate in _locale_candidates():
        matched = _match_supported_language(candidate)
        if matched:
            return matched
    return _FALLBACK_LANGUAGE


def set_language(lang_code: str) -> None:
    """Load translations for the given language code.

    Args:
        lang_code: One of the supported language codes.
    """
    global _current_translator, _current_language

    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = _FALLBACK_LANGUAGE

    try:
        _current_translator = gettext.translation(
            "messages",
            localedir=str(LOCALES_DIR),
            languages=[lang_code],
            fallback=True,
        )
    except (OSError, FileNotFoundError):
        _current_translator = gettext.NullTranslations()

    _current_language = lang_code


def get_current_language() -> str:
    """Return the currently active language code."""
    return _current_language


def _(message: str) -> str:
    """Translate a message using the active locale.

    Args:
        message: The source message in English.

    Returns:
        The translated message, or the original if no translation exists.
    """
    global _current_translator
    if _current_translator is None:
        set_language(detect_system_language())
    return _current_translator.gettext(message)
