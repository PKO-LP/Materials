INSERT INTO questions (id, question, answer_1, answer_2, answer_3, answer_4, correct)
VALUES
(1, 'Какой запрос читает данные?', 'SELECT', 'INSERT', 'UPDATE', 'CREATE', 1),
(2, 'Какое слово указывает таблицу в SELECT?', 'ORDER', 'FROM', 'VALUES', 'SET', 2),
(3, 'Какой запрос добавляет строку?', 'DROP', 'SELECT', 'INSERT', 'WHERE', 3),
(4, 'Какой тип хранит целое число?', 'DATE', 'TEXT', 'NUMERIC', 'INTEGER', 4),
(5, 'Как сортировать по возрастанию?', 'ASC', 'DESC', 'NULL', 'CHECK', 1)
ON CONFLICT (id) DO NOTHING;
