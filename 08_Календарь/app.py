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
    return прочитать("SELECT title, event_date FROM public.demo_events ORDER BY event_date, title")


def найти():
    try:
        текст = поле.get().strip()
        день = date.fromisoformat(текст)
        if день.isoformat() != текст:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Дата", "Введите существующую дату ГГГГ-ММ-ДД.", parent=окно)
        return
    return прочитать("SELECT title, event_date FROM public.demo_events WHERE event_date = %s ORDER BY title", (день,))

окно = tk.Tk()
окно.title('Календарь мероприятий')
окно.geometry("740x430")
ttk.Label(окно, text='Дата: например 2026-10-30').pack(pady=8)
поле = ttk.Entry(окно, width=35)
поле.pack(pady=5)
панель = ttk.Frame(окно)
панель.pack(pady=8)
кнопка_1 = ttk.Button(панель, text='Найти дату', command=найти)
кнопка_1.pack(side="left", padx=5)
кнопка_2 = ttk.Button(панель, text='Все события', command=все)
кнопка_2.pack(side="left", padx=5)
кнопка_3 = ttk.Button(панель, text='Очистить виджет', command=очистить)
кнопка_3.pack(side="left", padx=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
таблица = ttk.Treeview(область, columns=('title', 'event_date'), show="headings", height=4)
таблица.heading('title', text='Мероприятие')
таблица.column('title', width=220, anchor="center")
таблица.heading('event_date', text='Дата')
таблица.column('event_date', width=220, anchor="center")
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="Выберите действие")
статус.pack(pady=5)
все()
окно.mainloop()
