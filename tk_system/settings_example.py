# Скопируйте в settings.py и укажите свой пароль PostgreSQL.
DB = dict(dbname="final_up_shared",user="postgres",password="ВАШ_ПАРОЛЬ",
          host="localhost",port=5432,connect_timeout=5,
          options="-c statement_timeout=5000")
