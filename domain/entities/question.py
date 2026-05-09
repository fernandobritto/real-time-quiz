"""Domain entity representing a single quiz question."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """Immutable domain entity for a quiz question."""

    id: int
    question: str
    alternatives: list[str]
    correct_answer: str
