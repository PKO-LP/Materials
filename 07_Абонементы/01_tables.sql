-- Выполнить в базе mini_plans.
CREATE TABLE IF NOT EXISTS public.demo_plans (plan_name TEXT PRIMARY KEY, fee NUMERIC(8,2) NOT NULL CHECK (fee >= 0));
