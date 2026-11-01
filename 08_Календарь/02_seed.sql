-- Выполнить в базе mini_events.
INSERT INTO public.demo_events VALUES ('Лекция', '2026-10-30'), ('Практикум', '2026-10-30'), ('Выставка', '2026-11-01') ON CONFLICT DO NOTHING;
