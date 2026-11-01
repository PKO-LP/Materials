-- Выполнить в базе mini_plans.
INSERT INTO public.demo_plans VALUES ('Пробный', 0.00), ('Старт', 500.50), ('Месяц', 1500.00), ('Сезон', 4000.00) ON CONFLICT DO NOTHING;
