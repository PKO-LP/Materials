import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB

def найти():
    название = поле.get().strip()
    if not название:
        messagebox.showwarning("Проверка", "Введите название курса.", parent=окно)
        return
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("SELECT teacher_name FROM public.demo_courses WHERE title = %s", (название,))
                запись = курсор.fetchone()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    if запись is None:
        ответ.config(text="Такого курса нет")
    else:
        ответ.config(text="Преподаватель: " + запись[0])


окно = tk.Tk()
окно.title("Карточка учебного курса")
окно.geometry("600x250")
ttk.Label(окно, text="Название: Python, SQL или Рисование").pack(pady=10)
поле = ttk.Entry(окно, width=35)
поле.pack(pady=5)
кнопка_поиска = ttk.Button(окно, text="Показать преподавателя", command=найти)
кнопка_поиска.pack(pady=10)
ответ = ttk.Label(окно, text="Здесь будет один найденный ответ")
ответ.pack(pady=10)
окно.mainloop()
