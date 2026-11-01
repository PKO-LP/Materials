-- Выполнить в базе mini_notes.
CREATE TABLE IF NOT EXISTS public.demo_notes (title TEXT PRIMARY KEY CHECK (btrim(title) <> ''));
