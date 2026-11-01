-- Выполнить в базе mini_visits.
CREATE TABLE IF NOT EXISTS public.demo_visits (visitor_name TEXT NOT NULL, visit_date DATE NOT NULL, PRIMARY KEY (visitor_name, visit_date));
