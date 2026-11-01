-- Выполнить в базе mini_clubs.
INSERT INTO public.demo_clubs VALUES ('Робототехника', 'Понедельник'), ('Рисование', 'Среда'), ('Шахматы', 'Понедельник') ON CONFLICT DO NOTHING;
