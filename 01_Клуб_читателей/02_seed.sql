-- Выполнить в базе mini_reading_club.
INSERT INTO public.demo_access VALUES (1, 'd44b2ffcac07bdaf3f818c2dff630b97:48a7b56ad854609016799d228f7931e2b171ec3820462540a1fb88284b7f0455') ON CONFLICT DO NOTHING;
INSERT INTO public.demo_books VALUES ('Муму'), ('Каштанка'), ('Детство') ON CONFLICT DO NOTHING;
