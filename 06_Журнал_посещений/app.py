import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB
from datetime import date

def очистить():
    for строка in таблица.get_children():
        таблица.delete(строка)


def прочитать(sql, параметры=()):
    # Сначала читаем БД. Только после успеха изменяем содержимое окна.
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute(sql, параметры)
                записи = курсор.fetchall()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return False
    очистить()
    for запись in записи:
        таблица.insert("", tk.END, values=запись)
    статус.config(text=f"Найдено записей: {len(записи)}")
    return True

def все():
    return прочитать("SELECT visitor_name, visit_date FROM public.demo_visits ORDER BY visit_date, visitor_name")


def отметить():
    имя = поле.get().strip()
    if not имя:
        messagebox.showwarning("Проверка", "Введите учебное имя.", parent=окно)
        return
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("INSERT INTO public.demo_visits VALUES (%s, %s)", (имя, date.today()))
    except psycopg.errors.UniqueViolation:
        messagebox.showwarning("Повтор", "Это имя уже отмечено сегодня.", parent=окно)
        return
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    поле.delete(0, tk.END)
    все()

окно = tk.Tk()
окно.title('Журнал посещений')
окно.geometry("740x430")
ttk.Label(окно, text='Учебное имя; дата подставится автоматически').pack(pady=8)
поле = ttk.Entry(окно, width=35)
поле.pack(pady=5)
панель = ttk.Frame(окно)
панель.pack(pady=8)
кнопка_1 = ttk.Button(панель, text='Отметить сегодня', command=отметить)
кнопка_1.pack(side="left", padx=5)
кнопка_2 = ttk.Button(панель, text='Показать журнал', command=все)
кнопка_2.pack(side="left", padx=5)
кнопка_3 = ttk.Button(панель, text='Очистить виджет', command=очистить)
кнопка_3.pack(side="left", padx=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
таблица = ttk.Treeview(область, columns=('visitor_name', 'visit_date'), show="headings", height=4)
таблица.heading('visitor_name', text='Имя')
таблица.column('visitor_name', width=220, anchor="center")
таблица.heading('visit_date', text='Дата')
таблица.column('visit_date', width=220, anchor="center")
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="Выберите действие")
статус.pack(pady=5)
все()
окно.mainloop()
