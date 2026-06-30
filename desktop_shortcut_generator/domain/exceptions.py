"""Custom domain exceptions for Desktop Shortcut Generator."""


class DomainError(Exception):
    """Base exception for all domain-level errors."""


class ValidationError(DomainError):
    """Raised when shortcut data fails validation.

    Attributes:
        field: The name of the field that failed validation.
        message: A human-readable error description.
    """

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(message)


class FileWriteError(DomainError):
    """Raised when writing a .desktop file to disk fails."""
