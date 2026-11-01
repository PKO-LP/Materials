CREATE TABLE IF NOT EXISTS public.shop_users (
    login TEXT PRIMARY KEY CHECK (length(login) BETWEEN 3 AND 30),
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.shop_products (
    title TEXT NOT NULL CHECK (btrim(title) <> ''),
    category TEXT NOT NULL CHECK (btrim(category) <> ''),
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    received_on DATE NOT NULL,
    PRIMARY KEY (title, category)
);
