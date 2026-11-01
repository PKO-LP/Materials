-- Выполнить в базе mini_teams.
CREATE TABLE IF NOT EXISTS public.demo_teams (team_name TEXT PRIMARY KEY, points INTEGER NOT NULL CHECK (points >= 0));
