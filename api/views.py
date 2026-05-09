"""API views for fetching questions and submitting answers."""
import json
import uuid

from django.http import JsonResponse
from django.views import View

from domain.exceptions import InvalidQuizDataError
from infra.repositories.json_quiz_repository import JsonQuizRepository
from services import answer_validator
from services.quiz_service import QuizService

SESSION_KEY_SEED = "quiz_seed"
SESSION_KEY_SCORE = "quiz_score"
SESSION_KEY_ANSWERS = "quiz_answers"

_repository = JsonQuizRepository()
_service = QuizService(_repository)


def _init_session(session) -> None:
    """Initialise quiz session keys if not already present."""
    if SESSION_KEY_SEED not in session:
        session[SESSION_KEY_SEED] = uuid.uuid4().hex
    if SESSION_KEY_SCORE not in session:
        session[SESSION_KEY_SCORE] = 0
    if SESSION_KEY_ANSWERS not in session:
        session[SESSION_KEY_ANSWERS] = {}


class QuestionView(View):
    """Return the question at the given index as JSON."""

    def get(self, request, index: int) -> JsonResponse:
        _init_session(request.session)
        seed: str = request.session[SESSION_KEY_SEED]

        total = _service.get_total_count()
        if index < 0 or index >= total:
            return JsonResponse({"error": "Question index out of range."}, status=404)

        try:
            dto = _service.get_question(index, seed)
        except InvalidQuizDataError as exc:
            return JsonResponse({"error": str(exc)}, status=500)

        return JsonResponse({
            "id": dto.id,
            "question": dto.question,
            "alternatives": dto.alternatives,
            "index": dto.index,
            "total": dto.total,
        })


class AnswerView(View):
    """Accept a submitted answer, validate it, and update session state."""

    def post(self, request) -> JsonResponse:
        try:
            body: dict = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)

        question_id = body.get("question_id")
        selected = body.get("selected")

        if question_id is None or selected is None:
            return JsonResponse(
                {"error": "Both 'question_id' and 'selected' are required."}, status=400
            )

        _init_session(request.session)

        try:
            questions = _repository.get_all_questions()
        except InvalidQuizDataError as exc:
            return JsonResponse({"error": str(exc)}, status=500)

        matching = [q for q in questions if q.id == question_id]
        if not matching:
            return JsonResponse({"error": "Question not found."}, status=404)

        question = matching[0]
        result = answer_validator.validate_answer(question, selected)

        answers: dict = request.session.get(SESSION_KEY_ANSWERS, {})
        answers[str(question_id)] = {
            "selected": selected,
            "is_correct": result[answer_validator.ANSWER_KEY_IS_CORRECT],
            "correct_answer": result[answer_validator.ANSWER_KEY_CORRECT_ANSWER],
        }
        request.session[SESSION_KEY_ANSWERS] = answers

        if result[answer_validator.ANSWER_KEY_IS_CORRECT]:
            request.session[SESSION_KEY_SCORE] = (
                request.session.get(SESSION_KEY_SCORE, 0) + 1
            )

        request.session.modified = True

        return JsonResponse({
            "is_correct": result[answer_validator.ANSWER_KEY_IS_CORRECT],
            "correct_answer": result[answer_validator.ANSWER_KEY_CORRECT_ANSWER],
        })

        return JsonResponse({
            "is_correct": result[answer_validator.ANSWER_KEY_IS_CORRECT],
            "correct_answer": result[answer_validator.ANSWER_KEY_CORRECT_ANSWER],
        })
