-- Выполнять в базе mini_member_form.
CREATE TABLE IF NOT EXISTS public.demo_members (
    member_name TEXT NOT NULL CHECK (btrim(member_name) <> ''),
    group_name TEXT NOT NULL CHECK (btrim(group_name) <> ''),
    fee NUMERIC(10,2) NOT NULL CHECK (fee > 0),
    points INTEGER NOT NULL CHECK (points >= 0),
    joined_on DATE NOT NULL,
    PRIMARY KEY (member_name, group_name)
);
