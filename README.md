# Real-Time Quiz

A Django-based online quiz application following Clean Architecture principles. Questions are loaded from a JSON file — no database required.

## Requirements

- Python 3.11+
- Django 4.2+

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000/**

## Architecture

```
domain/      — Entities, DTOs, interfaces, exceptions (no framework imports)
services/    — Business rules: quiz flow orchestration, answer validation
infra/       — JSON repository implementation, quiz data file
api/         — REST endpoints (GET /api/question/<index>/, POST /api/answer/)
web/         — Django templates, static CSS/JS, page views
```

## Quiz Data

Questions are stored in `infra/data/questions.json`. You can add or modify questions there — the file is validated against a JSON schema on first load.

## Running with a custom questions file

Replace `infra/data/questions.json` with your own file. Each question must follow:

```json
{
  "id": 1,
  "question": "Your question here?",
  "alternatives": ["Option A", "Option B", "Option C"],
  "correctAnswer": "Option A"
}
```
