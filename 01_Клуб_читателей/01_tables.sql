-- Выполнить в базе mini_reading_club.
CREATE TABLE IF NOT EXISTS public.demo_access (id INTEGER PRIMARY KEY CHECK (id = 1), code_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS public.demo_books (title TEXT PRIMARY KEY);
