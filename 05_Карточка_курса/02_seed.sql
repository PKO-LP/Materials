-- Выполнить в базе mini_courses.
INSERT INTO public.demo_courses VALUES ('Python', 'Анна'), ('SQL', 'Борис'), ('Рисование', 'Вера') ON CONFLICT DO NOTHING;
