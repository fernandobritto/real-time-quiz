"""Data Transfer Object for a quiz question, ready for API/template use."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionDTO:
    """Serialisable representation of a question with shuffled alternatives."""

    id: int
    question: str
    alternatives: list[str]
    index: int
    total: int
