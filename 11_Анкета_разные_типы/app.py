import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from datetime import date
import psycopg
from settings import DB


def показать():
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("SELECT member_name, group_name, fee, points, joined_on FROM public.demo_members ORDER BY member_name, group_name")
                записи = курсор.fetchall()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return False
    for строка in таблица.get_children():
        таблица.delete(строка)
    for имя, группа, сумма, баллы, дата in записи:
        таблица.insert("", tk.END, values=(имя, группа, f"{сумма:.2f}", баллы, дата.isoformat()))
    статус.config(text=f"Участников: {len(записи)}")
    return True


def добавить():
    имя = поле_имени.get().strip()
    группа = поле_группы.get().strip()
    if not имя or not группа:
        messagebox.showwarning("Проверка", "Введите имя и группу.", parent=окно)
        return
    try:
        сумма = Decimal(поле_суммы.get().strip().replace(",", "."))
        if not сумма.is_finite() or not Decimal("0.01") <= сумма <= Decimal("99999999.99"):
            raise ValueError
        if сумма != сумма.quantize(Decimal("0.01")):
            raise ValueError
    except (ValueError, InvalidOperation):
        messagebox.showwarning("Сумма", "Положительная сумма до 99999999.99, максимум две значащие цифры после точки.", parent=окно)
        return
    try:
        баллы = int(поле_баллов.get().strip())
        if not 0 <= баллы <= 2147483647:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Баллы", "Целое число от 0 до 2147483647.", parent=окно)
        return
    try:
        текст_даты = поле_даты.get().strip()
        дата = date.fromisoformat(текст_даты)
        if дата.isoformat() != текст_даты:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Дата", "Существующая дата в формате ГГГГ-ММ-ДД.", parent=окно)
        return
    данные = (имя, группа, сумма, баллы, дата)
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute("""INSERT INTO public.demo_members
                    (member_name, group_name, fee, points, joined_on)
                    VALUES (%s, %s, %s, %s, %s)""", данные)
    except psycopg.errors.UniqueViolation:
        messagebox.showwarning("Повтор", "Участник с таким именем в этой группе уже есть.", parent=окно)
        return
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return
    # Новое подключение для SELECT — только после успешного сохранения INSERT.
    for поле in поля:
        поле.delete(0, tk.END)
    поле_даты.insert(0, date.today().isoformat())
    if показать():
        статус.config(text="Анкета сохранена, данные заново прочитаны из БД.")
    else:
        статус.config(text="Анкета сохранена. Повторите «Показать» для обновления.")


окно = tk.Tk()
окно.title("Анкета участника — разные типы данных")
окно.geometry("900x520")
форма = ttk.Frame(окно, padding=10)
форма.pack(fill="x")
форма.columnconfigure(1, weight=1)
поля = []
подписи = ("Имя", "Учебная группа", "Взнос, руб.", "Баллы", "Дата: ГГГГ-ММ-ДД")
for номер, подпись in enumerate(подписи):
    ttk.Label(форма, text=подпись).grid(row=номер, column=0, sticky="w", pady=4)
    поле = ttk.Entry(форма)
    поле.grid(row=номер, column=1, sticky="ew", padx=10)
    поля.append(поле)
поле_имени, поле_группы, поле_суммы, поле_баллов, поле_даты = поля
поле_даты.insert(0, date.today().isoformat())
кнопка_добавить = ttk.Button(окно, text="Сохранить анкету", command=добавить)
кнопка_добавить.pack(pady=5)
кнопка_показать = ttk.Button(окно, text="Показать", command=показать)
кнопка_показать.pack(pady=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
столбцы = ("member_name", "group_name", "fee", "points", "joined_on")
таблица = ttk.Treeview(область, columns=столбцы, show="headings", height=3)
for имя_столбца, подпись in zip(столбцы, подписи):
    таблица.heading(имя_столбца, text=подпись)
    таблица.column(имя_столбца, width=155)
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="")
статус.pack(pady=5)
показать()
окно.mainloop()
