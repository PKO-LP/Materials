import tkinter as tk
from tkinter import ttk, messagebox
import psycopg
from settings import DB
from decimal import Decimal, InvalidOperation

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
    return прочитать("SELECT plan_name, fee FROM public.demo_plans ORDER BY fee ASC, plan_name")


def не_дороже():
    try:
        предел = Decimal(поле.get().strip().replace(",", "."))
        if not предел.is_finite() or not Decimal("0") <= предел <= Decimal("999999.99"):
            raise ValueError
        if предел != предел.quantize(Decimal("0.01")):
            raise ValueError
    except (ValueError, InvalidOperation):
        messagebox.showwarning("Проверка", "Введите сумму от 0 до 999999.99, до двух знаков после точки.", parent=окно)
        return
    return прочитать("SELECT plan_name, fee FROM public.demo_plans WHERE fee <= %s ORDER BY fee ASC, plan_name", (предел,))


def дорогие():
    return прочитать("SELECT plan_name, fee FROM public.demo_plans ORDER BY fee DESC, plan_name")

окно = tk.Tk()
окно.title('Абонементы секций')
окно.geometry("740x430")
ttk.Label(окно, text='Максимальная стоимость, руб.').pack(pady=8)
поле = ttk.Entry(окно, width=35)
поле.pack(pady=5)
панель = ttk.Frame(окно)
панель.pack(pady=8)
кнопка_1 = ttk.Button(панель, text='Не дороже', command=не_дороже)
кнопка_1.pack(side="left", padx=5)
кнопка_2 = ttk.Button(панель, text='Все по возрастанию', command=все)
кнопка_2.pack(side="left", padx=5)
кнопка_3 = ttk.Button(панель, text='Все по убыванию', command=дорогие)
кнопка_3.pack(side="left", padx=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
таблица = ttk.Treeview(область, columns=('plan_name', 'fee'), show="headings", height=4)
таблица.heading('plan_name', text='Абонемент')
таблица.column('plan_name', width=220, anchor="center")
таблица.heading('fee', text='Стоимость')
таблица.column('fee', width=220, anchor="center")
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="Выберите действие")
статус.pack(pady=5)
все()
окно.mainloop()
