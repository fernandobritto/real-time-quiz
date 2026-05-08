"""Infrastructure implementation of QuizRepositoryInterface using a JSON file."""
import json
from pathlib import Path

import jsonschema

from domain.entities.question import Question
from domain.exceptions import InvalidQuizDataError
from domain.interfaces.quiz_repository import QuizRepositoryInterface

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "questions.json"

_QUIZ_SCHEMA: dict = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["questions"],
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "question", "alternatives", "correctAnswer"],
                "properties": {
                    "id": {"type": "integer"},
                    "question": {"type": "string", "minLength": 5},
                    "alternatives": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 5,
                        "items": {"type": "string"},
                    },
                    "correctAnswer": {"type": "string"},
                },
            },
        }
    },
}

# Module-level cache: populated on first call to get_all_questions()
_cache: list[Question] | None = None


class JsonQuizRepository(QuizRepositoryInterface):
    """Reads quiz questions from a JSON file and validates them against the schema."""

    def get_all_questions(self) -> list[Question]:
        """Return all questions, loading and validating from disk on the first call."""
        global _cache
        if _cache is None:
            _cache = self._load()
        return _cache

    def _load(self) -> list[Question]:
        """Read, parse, validate, and convert the JSON data file."""
        if not _DATA_FILE.exists():
            raise InvalidQuizDataError(
                f"Quiz data file not found: {_DATA_FILE}"
            )

        try:
            raw = json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise InvalidQuizDataError(
                f"Quiz data file contains invalid JSON: {exc}"
            ) from exc

        try:
            jsonschema.validate(instance=raw, schema=_QUIZ_SCHEMA)
        except jsonschema.ValidationError as exc:
            raise InvalidQuizDataError(
                f"Quiz data failed schema validation: {exc.message}"
            ) from exc

        return [
            Question(
                id=item["id"],
                question=item["question"],
                alternatives=list(item["alternatives"]),
                correct_answer=item["correctAnswer"],
            )
            for item in raw["questions"]
        ]
