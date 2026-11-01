-- Выполнить в базе mini_teams.
INSERT INTO public.demo_teams VALUES ('Альфа', 3), ('Бета', 8), ('Гамма', 12), ('Дельта', 8) ON CONFLICT DO NOTHING;
