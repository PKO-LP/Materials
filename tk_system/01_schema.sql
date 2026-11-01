CREATE TABLE IF NOT EXISTS users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name TEXT NOT NULL CHECK (btrim(full_name) <> ''),
    login TEXT NOT NULL CHECK (length(login) BETWEEN 3 AND 50),
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Ученик','Преподаватель'))
);
CREATE UNIQUE INDEX IF NOT EXISTS users_login_lower_unique ON users (lower(login));

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    position INTEGER UNIQUE NOT NULL CHECK (position BETWEEN 1 AND 5),
    question_text TEXT NOT NULL CHECK (btrim(question_text) <> ''),
    option_1 TEXT NOT NULL CHECK (btrim(option_1) <> ''),
    option_2 TEXT NOT NULL CHECK (btrim(option_2) <> ''),
    option_3 TEXT NOT NULL CHECK (btrim(option_3) <> ''),
    option_4 TEXT NOT NULL CHECK (btrim(option_4) <> ''),
    correct_option INTEGER NOT NULL CHECK (correct_option BETWEEN 1 AND 4)
);
CREATE TABLE IF NOT EXISTS attempts (
    id UUID PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id),
    finished_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    correct_count INTEGER NOT NULL CHECK (correct_count BETWEEN 0 AND 5),
    grade INTEGER NOT NULL CHECK (grade BETWEEN 2 AND 5)
);
CREATE TABLE IF NOT EXISTS answers (
    attempt_id UUID NOT NULL REFERENCES attempts(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    position INTEGER NOT NULL CHECK (position BETWEEN 1 AND 5),
    question_text TEXT NOT NULL,
    option_1 TEXT NOT NULL,
    option_2 TEXT NOT NULL,
    option_3 TEXT NOT NULL,
    option_4 TEXT NOT NULL,
    chosen_option INTEGER NOT NULL CHECK (chosen_option BETWEEN 1 AND 4),
    correct_option INTEGER NOT NULL CHECK (correct_option BETWEEN 1 AND 4),
    PRIMARY KEY (attempt_id,position)
);
