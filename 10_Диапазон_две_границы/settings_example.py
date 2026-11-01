# Скопируйте этот файл в settings.py и укажите свои параметры PostgreSQL.
DB = dict(dbname='mini_price_range', user="postgres", password="ВАШ_ПАРОЛЬ",
          host="localhost", port=5432, connect_timeout=5,
          options="-c statement_timeout=5000")
