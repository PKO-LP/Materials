import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
import psycopg
from settings import DB


def прочитать_цену(текст):
    число = Decimal(текст.strip().replace(",", "."))
    if not число.is_finite() or not Decimal("0") <= число <= Decimal("999999.99"):
        raise ValueError
    if число != число.quantize(Decimal("0.01")):
        raise ValueError
    return число


def очистить():
    for строка in таблица.get_children():
        таблица.delete(строка)


def загрузить(по_убыванию=False):
    try:
        нижняя = прочитать_цену(поле_от.get()) if поле_от.get().strip() else Decimal("0")
        верхняя = прочитать_цену(поле_до.get()) if поле_до.get().strip() else Decimal("999999.99")
        if нижняя > верхняя:
            raise ValueError
    except (ValueError, InvalidOperation):
        messagebox.showwarning("Диапазон", "Две цены от 0 до 999999.99, до двух знаков. От не больше До.", parent=окно)
        return False
    sql = "SELECT title, fee FROM public.demo_workshops WHERE fee BETWEEN %s AND %s"
    if по_убыванию:
        sql += " ORDER BY fee DESC, title ASC"
    else:
        sql += " ORDER BY fee ASC, title ASC"
    try:
        with psycopg.connect(**DB) as соединение:
            with соединение.cursor() as курсор:
                курсор.execute(sql, (нижняя, верхняя))
                записи = курсор.fetchall()
    except psycopg.Error as ошибка:
        messagebox.showerror("База данных", str(ошибка), parent=окно)
        return False
    очистить()
    for название, цена in записи:
        таблица.insert("", tk.END, values=(название, f"{цена:.2f}"))
    статус.config(text=f"Найдено: {len(записи)}")
    return True


def по_возрастанию():
    return загрузить(False)


def по_убыванию():
    return загрузить(True)


def все():
    поле_от.delete(0, tk.END)
    поле_до.delete(0, tk.END)
    return загрузить()


окно = tk.Tk()
окно.title("Стоимость мастер-классов: диапазон")
окно.geometry("720x390")
фильтр = ttk.Frame(окно, padding=10)
фильтр.pack(fill="x")
ttk.Label(фильтр, text="От, руб.").pack(side="left")
поле_от = ttk.Entry(фильтр, width=14)
поле_от.pack(side="left", padx=8)
ttk.Label(фильтр, text="До, руб.").pack(side="left")
поле_до = ttk.Entry(фильтр, width=14)
поле_до.pack(side="left", padx=8)
кнопки = ttk.Frame(окно)
кнопки.pack(pady=8)
кнопка_возрастания = ttk.Button(кнопки, text="Отобрать: дешевле → дороже", command=по_возрастанию)
кнопка_возрастания.pack(side="left", padx=5)
кнопка_убывания = ttk.Button(кнопки, text="Отобрать: дороже → дешевле", command=по_убыванию)
кнопка_убывания.pack(side="left", padx=5)
кнопка_все = ttk.Button(кнопки, text="Все", command=все)
кнопка_все.pack(side="left", padx=5)
область = ttk.Frame(окно)
область.pack(fill="x", padx=15, pady=10)
таблица = ttk.Treeview(область, columns=("title", "fee"), show="headings", height=3)
таблица.heading("title", text="Мастер-класс")
таблица.heading("fee", text="Цена, руб.")
полоса = ttk.Scrollbar(область, orient="vertical", command=таблица.yview)
таблица.configure(yscrollcommand=полоса.set)
полоса.pack(side="right", fill="y")
таблица.pack(side="left", fill="x", expand=True)
статус = ttk.Label(окно, text="")
статус.pack(pady=5)
все()
окно.mainloop()
