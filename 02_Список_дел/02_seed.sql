-- Выполнить в базе mini_notes.
INSERT INTO public.demo_notes VALUES ('Прочитать главу'), ('Повторить SQL'), ('Проверить конспект') ON CONFLICT DO NOTHING;
