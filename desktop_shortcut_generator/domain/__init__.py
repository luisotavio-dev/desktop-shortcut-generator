"""Domain layer containing business rules and entities."""

from desktop_shortcut_generator.domain.entities import Shortcut
from desktop_shortcut_generator.domain.exceptions import (
    DomainError,
    FileWriteError,
    ValidationError,
)

__all__ = [
    "DomainError",
    "FileWriteError",
    "Shortcut",
    "ValidationError",
]
