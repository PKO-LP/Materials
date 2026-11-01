-- Выполнить в базе mini_visits.
INSERT INTO public.demo_visits VALUES ('Участник А', '2026-10-01'), ('Участник Б', '2026-10-02') ON CONFLICT DO NOTHING;
