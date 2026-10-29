# WikiAutomation
Demo for ways to automate wiki

This repository holds a small Flask website for an **AI Engineer Course on Microsoft Agent Framework**. It is a
deliberately unfinished (about 10%) project, used as a realistic codebase to demonstrate automated wiki maintenance.

## Status: about 10% complete

| Part | State |
|---|---|
| Course catalogue and module pages | Done |
| Module 1: What is an AI agent? (3 lessons, runnable workflow example) | Done |
| Modules 2-10 | Planned ("coming soon" pages) |
| JSON API: modules, enrolment | Done |
| Database schema: learners, enrolments, lesson progress | Done (progress not used yet) |
| Sign-up page, login, progress tracking, quizzes, certificates | Not started |

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\flask --app app run --debug      # http://localhost:5000
```

## Roadmap

1. Modules 2-10 content (chat clients, tools, state, workflows, human in the loop, multi-agent, AG-UI, evaluation, capstone)
2. Sign-up page backed by `POST /api/enrollments`
3. Lesson progress (`lesson_progress` table) with a progress API
4. Quizzes per module
5. Authentication for learners
