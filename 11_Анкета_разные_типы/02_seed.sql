INSERT INTO public.demo_members VALUES ('Анна', 'А', 100.50, 3, '2026-10-01'), ('Борис', 'Б', 200, 5, '2026-10-02') ON CONFLICT DO NOTHING;
