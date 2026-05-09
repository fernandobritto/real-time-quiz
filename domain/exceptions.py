"""Domain-level exceptions for the quiz application."""


class InvalidQuizDataError(Exception):
    """Raised when quiz data is missing, malformed, or fails schema validation."""
