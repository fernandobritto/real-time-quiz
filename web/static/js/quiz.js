/* global TOTAL – injected by Django template */
"use strict";

(function () {
  const RESULT_URL = "/quiz/result/";
  const API_QUESTION_BASE = "/api/question/";
  const API_ANSWER_URL = "/api/answer/";

  let currentIndex = 0;
  let totalQuestions = typeof TOTAL !== "undefined" ? TOTAL : 0;
  let answerSubmitted = false;

  const progressEl = document.getElementById("progress");
  const questionEl = document.getElementById("question-text");
  const listEl = document.getElementById("alternatives-list");
  const nextBtn = document.getElementById("next-btn");
  const errorCard = document.getElementById("error-card");
  const errorMsg = document.getElementById("error-message");
  const quizCard = document.getElementById("quiz-card");

  function getCsrfToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      const [key, val] = cookie.trim().split("=");
      if (key === name) return decodeURIComponent(val);
    }
    return "";
  }

  function showError(message) {
    quizCard.classList.add("hidden");
    errorCard.classList.remove("hidden");
    errorMsg.textContent = message;
  }

  function setProgress(index, total) {
    progressEl.textContent = `Question ${index + 1} of ${total}`;
  }

  function renderAlternatives(alternatives, questionId) {
    listEl.innerHTML = "";
    alternatives.forEach((text) => {
      const li = document.createElement("li");
      li.setAttribute("role", "listitem");

      const btn = document.createElement("button");
      btn.className = "alternative-btn";
      btn.textContent = text;
      btn.setAttribute("aria-label", `Select answer: ${text}`);

      btn.addEventListener("click", () =>
        handleAnswerSelect(btn, alternatives, questionId, text),
      );

      li.appendChild(btn);
      listEl.appendChild(li);
    });
  }

  async function handleAnswerSelect(
    selectedBtn,
    allAlternatives,
    questionId,
    selected,
  ) {
    if (answerSubmitted) return;
    answerSubmitted = true;

    // Mark selected before response
    selectedBtn.classList.add("alternative-btn--selected");

    // Disable all buttons
    const allBtns = listEl.querySelectorAll(".alternative-btn");
    allBtns.forEach((b) => {
      b.disabled = true;
      b.setAttribute("aria-disabled", "true");
    });

    let result;
    try {
      const response = await fetch(API_ANSWER_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({ question_id: questionId, selected }),
      });
      result = await response.json();
    } catch {
      showError(
        "Failed to submit answer. Please check your connection and refresh.",
      );
      return;
    }

    const { is_correct, correct_answer } = result;

    // Apply colour feedback
    allBtns.forEach((btn) => {
      btn.classList.remove("alternative-btn--selected");
      if (btn.textContent === correct_answer) {
        btn.classList.add("alternative-btn--correct");
      } else if (btn === selectedBtn && !is_correct) {
        btn.classList.add("alternative-btn--wrong");
      }
    });

    // Enable next button
    nextBtn.disabled = false;
    nextBtn.setAttribute("aria-disabled", "false");
  }

  async function loadQuestion(index) {
    answerSubmitted = false;
    nextBtn.disabled = true;
    nextBtn.setAttribute("aria-disabled", "true");
    listEl.innerHTML = "";
    questionEl.textContent = "";
    progressEl.textContent = "";

    let data;
    try {
      const response = await fetch(`${API_QUESTION_BASE}${index}/`);
      if (!response.ok) {
        showError("Could not load question. The quiz may have ended.");
        return;
      }
      data = await response.json();
    } catch {
      showError("Network error. Please refresh the page.");
      return;
    }

    totalQuestions = data.total;
    setProgress(data.index, data.total);
    questionEl.textContent = data.question;
    renderAlternatives(data.alternatives, data.id);
  }

  function handleNext() {
    if (!answerSubmitted) return;
    currentIndex += 1;
    if (currentIndex >= totalQuestions) {
      window.location.href = RESULT_URL;
    } else {
      loadQuestion(currentIndex);
    }
  }

  // Initialise
  nextBtn.addEventListener("click", handleNext);
  loadQuestion(currentIndex);
})();
