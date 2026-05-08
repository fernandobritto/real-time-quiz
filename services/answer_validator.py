"""Service responsible for validating a user's answer against the correct answer."""
from domain.entities.question import Question

ANSWER_KEY_IS_CORRECT = "is_correct"
ANSWER_KEY_CORRECT_ANSWER = "correct_answer"


def validate_answer(question: Question, selected: str) -> dict[str, bool | str]:
    """Return a structured validation result for the selected answer.

    Comparison is exact string equality (case-sensitive, whitespace-sensitive).
    """
    is_correct = selected == question.correct_answer
    return {
        ANSWER_KEY_IS_CORRECT: is_correct,
        ANSWER_KEY_CORRECT_ANSWER: question.correct_answer,
    }
