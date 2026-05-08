"""Web views: quiz page, result page, redirect, and restart."""
from django.shortcuts import redirect, render
from django.views import View

from api.views import SESSION_KEY_ANSWERS, SESSION_KEY_SCORE, SESSION_KEY_SEED
from domain.exceptions import InvalidQuizDataError
from infra.repositories.json_quiz_repository import JsonQuizRepository
from services.quiz_service import QuizService

_repository = JsonQuizRepository()
_service = QuizService(_repository)

_QUIZ_SESSION_KEYS = (SESSION_KEY_SEED, SESSION_KEY_SCORE, SESSION_KEY_ANSWERS)


class IndexRedirectView(View):
    """Redirect root URL to the quiz page."""

    def get(self, request):
        return redirect("web:quiz")


class QuizView(View):
    """Render the main quiz page."""

    def get(self, request):
        try:
            total = _service.get_total_count()
        except InvalidQuizDataError:
            return render(request, "500.html", status=500)

        answers: dict = request.session.get(SESSION_KEY_ANSWERS, {})
        if len(answers) >= total:
            return redirect("web:result")

        return render(request, "quiz/index.html", {"total": total})


class ResultView(View):
    """Render the quiz result page."""

    def get(self, request):
        answers: dict = request.session.get(SESSION_KEY_ANSWERS)
        if not answers:
            return redirect("web:quiz")

        try:
            questions = _repository.get_all_questions()
        except InvalidQuizDataError:
            return render(request, "500.html", status=500)

        total = len(questions)
        score: int = request.session.get(SESSION_KEY_SCORE, 0)
        percentage = round(score / total * 100) if total else 0

        breakdown = []
        for question in questions:
            answer_data = answers.get(str(question.id), {})
            breakdown.append({
                "question": question.question,
                "selected": answer_data.get("selected", "—"),
                "correct_answer": question.correct_answer,
                "is_correct": answer_data.get("is_correct", False),
            })

        # Clear quiz session data after collecting results
        for key in _QUIZ_SESSION_KEYS:
            request.session.pop(key, None)
        request.session.modified = True

        return render(request, "quiz/result.html", {
            "score": score,
            "total": total,
            "percentage": percentage,
            "breakdown": breakdown,
        })


class RestartView(View):
    """Clear quiz session state and redirect to the quiz start."""

    def get(self, request):
        for key in _QUIZ_SESSION_KEYS:
            request.session.pop(key, None)
        request.session.modified = True
        return redirect("web:quiz")
