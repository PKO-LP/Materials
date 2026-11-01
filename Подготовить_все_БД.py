"""Создание учебных баз на своём сервере. Сначала заполните settings.py в каждой папке."""
import json
import runpy
from pathlib import Path
import psycopg
from psycopg import sql

папка = Path(__file__).parent
for пример in json.loads((папка / "examples.json").read_text(encoding="utf-8")):
    путь = папка / пример["folder"]
    настройки = runpy.run_path(str(путь / "settings.py"))["DB"]
    администратор = dict(настройки)
    администратор["dbname"] = "postgres"
    with psycopg.connect(**администратор, autocommit=True) as соединение:
        with соединение.cursor() as курсор:
            курсор.execute("SELECT 1 FROM pg_database WHERE datname = %s", (настройки["dbname"],))
            if курсор.fetchone() is None:
                курсор.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(настройки["dbname"])))
    with psycopg.connect(**настройки) as соединение:
        with соединение.cursor() as курсор:
            курсор.execute((путь / "01_tables.sql").read_text(encoding="utf-8"))
            курсор.execute((путь / "02_seed.sql").read_text(encoding="utf-8"))
    print("Готово:", пример["db"])
