-- AI Engineer Course: storage for learners and enrolments.
-- Progress per lesson is planned (see README roadmap); the table is here so the API can grow into it.

CREATE TABLE IF NOT EXISTS learners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_id INTEGER NOT NULL REFERENCES learners(id),
    course TEXT NOT NULL,
    enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    learner_id INTEGER NOT NULL REFERENCES learners(id),
    module_slug TEXT NOT NULL,
    lesson_index INTEGER NOT NULL,
    completed_at TEXT,
    PRIMARY KEY (learner_id, module_slug, lesson_index)
);
