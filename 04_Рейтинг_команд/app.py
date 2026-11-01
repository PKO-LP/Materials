import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB

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
    return прочитать("SELECT team_name, points FROM public.demo_teams ORDER BY points ASC, team_name")


def найти():
    try:
        минимум = int(поле.get().strip())
        if not 0 <= минимум <= 2147483647:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Проверка", "Введите целое неотрицательное число до 2147483647.", parent=окно)
        return
    return прочитать("SELECT team_name, points FROM public.demo_teams WHERE points >= %s ORDER BY points ASC, team_name", (минимум,))


def лучшие():
    return прочитать("SELECT team_name, points FROM public.demo_teams ORDER BY points DESC, team_name")

окно = tk.Tk()
окно.title('Рейтинг команд')
окно.geometry("740x430")
ttk.Label(окно, text='Минимум баллов').pack(pady=8)
поле = ttk.Entry(окно, width=35)
поле.pack(pady=5)
панель = ttk.Frame(окно)
панель.pack(pady=8)
кнопка_1 = ttk.Button(панель, text='Отобрать', command=найти)
кнопка_1.pack(side="left", padx=5)
кнопка_2 = ttk.Button(панель, text='Все по возрастанию', command=все)
кнопка_2.pack(side="left", padx=5)
кнопка_3 = ttk.Button(панель, text='Все по убыванию', command=лучшие)
кнопка_3.pack(side="left", padx=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
таблица = ttk.Treeview(область, columns=('team_name', 'points'), show="headings", height=4)
таблица.heading('team_name', text='Команда')
таблица.column('team_name', width=220, anchor="center")
таблица.heading('points', text='Баллы')
таблица.column('points', width=220, anchor="center")
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="Выберите действие")
статус.pack(pady=5)
все()
окно.mainloop()
