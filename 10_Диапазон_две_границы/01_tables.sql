-- Выполнять в базе mini_price_range.
CREATE TABLE IF NOT EXISTS public.demo_workshops (title TEXT PRIMARY KEY, fee NUMERIC(8,2) NOT NULL CHECK (fee >= 0));
