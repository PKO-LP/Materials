-- Выполнять в базе mini_profiles.
CREATE TABLE IF NOT EXISTS public.demo_profiles (
    login TEXT PRIMARY KEY CHECK (length(login) BETWEEN 3 AND 30),
    password_hash TEXT NOT NULL
);
