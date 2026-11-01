INSERT INTO public.demo_workshops VALUES ('Открытая встреча', 0), ('Оригами', 250), ('Акварель', 500.50), ('Керамика', 750), ('Фотография', 1000), ('Печать', 1500) ON CONFLICT DO NOTHING;
