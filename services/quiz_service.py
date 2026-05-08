"""Service that orchestrates quiz flow: question retrieval and sequencing."""
import random

from domain.dto.question_dto import QuestionDTO
from domain.interfaces.quiz_repository import QuizRepositoryInterface


class QuizService:
    """Orchestrates quiz flow using an injected repository."""

    def __init__(self, repository: QuizRepositoryInterface) -> None:
        self._repository = repository

    def get_total_count(self) -> int:
        """Return the total number of questions in the quiz."""
        return len(self._repository.get_all_questions())

    def get_question(self, index: int, seed: str) -> QuestionDTO:
        """Return the question at *index* with alternatives shuffled by *seed*.

        The shuffle is deterministic for a given seed + question ID, so the
        order is stable across page refreshes within the same session.

        Raises IndexError if *index* is out of range.
        """
        questions = self._repository.get_all_questions()
        question = questions[index]
        total = len(questions)

        shuffled = list(question.alternatives)
        rng = random.Random(seed + str(question.id))
        rng.shuffle(shuffled)

        return QuestionDTO(
            id=question.id,
            question=question.question,
            alternatives=shuffled,
            index=index,
            total=total,
        )
