"""Abstract contract (port) for quiz data access."""
from abc import ABC, abstractmethod

from domain.entities.question import Question


class QuizRepositoryInterface(ABC):
    """Interface that all quiz data repositories must implement."""

    @abstractmethod
    def get_all_questions(self) -> list[Question]:
        """Return all quiz questions from the data source."""
        ...
